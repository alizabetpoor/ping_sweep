from scapy.all import sr1,ICMP,IP
import PySimpleGUI as sg
import threading


sg.theme("DarkBlue3")



def check_ip(start,end,networkrange,stop):
    
    window.refresh()
    window["progress"].UpdateBar(0,max=end-start)
    timeout=1
    window["-output-"].update("")
    i=0
    for host in range(start,end):
        if stop():
            break
        ip=networkrange+str(host)
        try:
            packet=IP(dst=ip) / ICMP()
            response=sr1(packet,timeout=timeout,verbose=0)
        except:
            break
        window["progress"].UpdateBar(i+1)
        i+=1
        if response:
            if response[ICMP].type==0:
                
                window["-output-"].print(f"{ip} is live")
                window.refresh()
    window.write_event_value("-end-task-","the thread has been end")

layout=[
        [sg.Text("give me network range:",font="Arial",border_width=2),sg.InputText("192.168.1.",font="Arial 12",key="-networkrange-")],
        [sg.Text("give me start number:",font="Arial",border_width=2),sg.InputText("1",font="Arial 12",key="-start-")],
        [sg.Text("give me end number:",font="Arial",border_width=2),sg.InputText("255",font="Arial 12",key="-end-")],
        [sg.Button("check ip",key="-check-ip-",font="Arial",size=(10,1)),sg.Button("stop",font="Arial",size=(10,1),key="-stop-")],
        [sg.Text("",visible=False,key="txt1",font='Arial',size=(20,20))],
        [sg.ProgressBar(2,orientation="h",size=(20,20),key="progress")],
        [sg.Multiline("",size=(30,10),font="Arial",auto_size_text=True,key="-output-",justification="left")],
]


stop_thread=False
window=sg.Window("PingSweep",layout,size=(500,300),element_justification="c")
thread=None
while True:
    event,inputstr=window.read()
    if event==sg.WIN_CLOSED:
        break
    elif event=="-stop-" and thread:
        stop_thread=True
    elif event=="-check-ip-" and not thread and \
        inputstr["-start-"].isdigit() and \
        inputstr["-end-"].isdigit() and \
        not inputstr["-networkrange-"].isalnum()    :

        start_range,end_range,networkrange=int(inputstr["-start-"])\
            ,int(inputstr["-end-"]),inputstr["-networkrange-"]
        thread=threading.Thread(target=check_ip,args=(start_range,end_range,networkrange,lambda : stop_thread),daemon=True)
        thread.start()
    elif event=="-end-task-":
        thread=None
        stop_thread=False
        
    
window.close()