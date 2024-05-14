import pandas as pd, numpy as np 
from collections import OrderedDict
import tkinter as tk
from tkinter import scrolledtext
from tkinter import filedialog
import difflib
import yaml
from jinja2 import Template

def show_message(message, font=("Arial", 10)):
    # Create Tkinter window
    window = tk.Tk()
    window.title("Message")

    # Create a label to display the message
    label = tk.Label(window, text=message, justify=tk.LEFT, font=font)
    label.pack(padx=20, pady=20)

    # Function to close the window
    def close_window():
        window.destroy()

    # Create an "OK" button to close the window
    ok_button = tk.Button(window, width=10,text="  OK  ", command=close_window)
    ok_button.pack(pady=10)
    window.mainloop()


def get_file_path():
    # Create Tkinter window
    window = tk.Tk()
    window.withdraw()  # Hide the main window

    # Open file selection dialog
    file_path = filedialog.askopenfilename()

    # Destroy the Tkinter window
    window.destroy()

    return file_path



def display_yaml_file(filename):
    # Create Tkinter window
    window = tk.Tk()
    window.title("YAML Viewer")

    # Create a scrolled text widget
    scroll_text = scrolledtext.ScrolledText(window, width=80, height=30, font=("Arial", 12))
    hindi_font = "Mangal"  # Example font that supports Hindi
    scroll_text.configure(font=(hindi_font, 12))  # Adjust the size as needed
    scroll_text.pack(expand=True, fill='both')

    try:
        # Read YAML file
        with open(filename, 'r', encoding='utf-8') as file:
            data = yaml.safe_load(file)
            # Display YAML data in the scrolled text widget
            scroll_text.insert(tk.END, yaml.dump(data, default_flow_style=False))
    except FileNotFoundError:
        scroll_text.insert(tk.END, "File not found!")
    except yaml.YAMLError as e:
        scroll_text.insert(tk.END, f"Error parsing YAML: {e}")

    # Run Tkinter main loop
    window.mainloop()

def read_text_file(file_path):
    try:
        with open(file_path, 'r', encoding='utf-8') as file:
            text_content = file.read()
        return text_content
    except FileNotFoundError:
        print("File not found!")
        return None
    except Exception as e:
        print("Error:", e)
        return None



def show_diff(text1, text2):
    print(text1,text2)
    # Generate the difference between the two texts
    differ = difflib.Differ()
    diff = list(differ.compare(text1.splitlines(keepends=True), text2.splitlines(keepends=True)))

    # Create Tkinter window
    window = tk.Tk()
    window.title("Text Difference")

    # Create a scrolled text widget to display the differences
    diff_text = scrolledtext.ScrolledText(window, width=80, height=30)
    diff_text.pack(expand=True, fill='both')

    # Display the differences in the scrolled text widget
    for line in diff:
        if line.startswith('+'):
            diff_text.insert(tk.END, line, 'added')
        elif line.startswith('-'):
            diff_text.insert(tk.END, line, 'deleted')
        elif line.startswith('?'):
            diff_text.insert(tk.END, line, 'modified')
        else:
            diff_text.insert(tk.END, line)

    # Configure tag styles for added, deleted, and modified lines
    diff_text.tag_config('added', foreground='green')
    diff_text.tag_config('deleted', foreground='red')
    diff_text.tag_config('modified', foreground='blue')

    window.mainloop()


def generate_diff_report(text1, text2, output_file):
    # Generate the difference between the two texts
    differ = difflib.HtmlDiff(wrapcolumn=80)
    diff_html = differ.make_file(text1.splitlines(), text2.splitlines())

    # Write the HTML diff report to the output file
    with open(output_file, 'w', encoding='utf-8') as file:
        file.write(diff_html)

    print("Diff report saved to", output_file)


def xlsxSurvey_to_Yaml(ip, op):
    df=pd.read_excel(ip, sheet_name='survey')
    choices=pd.read_excel(ip, sheet_name='choices')
    setdf=pd.read_excel(ip, sheet_name='settings')

    setdf=setdf[['form_title','form_id']]
    setdfT=setdf.T
    setdfT=setdfT[[0]]
    setdfT=setdfT.dropna()
    setdfT=setdfT.to_dict()[0]
    setdfT['form_file']=ip
    
    md=[setdfT]

    dfT=df.T   
    for i in range(len(df)):
        keyw=str((df.iloc[i,0])).split()
               
        tmpdf=dfT[[i]]
        tmpdf=tmpdf.dropna()
        td=tmpdf.to_dict()[i]
        

        if len(keyw)>1:
            # print(keyw[1])
            tmpch=(choices[['name','label']][choices['list_name']==keyw[1]]).head(30)
            tmpch.columns=['Code','Label']
            
            tmpch.index=['Option'+str(oi) for oi in range(1,len(tmpch)+1)]
            td['Option_List::'+keyw[1]]=tmpch.T.to_dict()
            
       

        # print(td)
        if(len(td)>0):
            md=md+[td]

        

    # Write the dictionary to a YAML file
    with open(op, 'w', encoding='utf-8') as yaml_file:
        # yaml.dump(df.to_dict(orient='records'), file, allow_unicode=True, default_flow_style=False, indent=4)
        for d in md:
            yaml_file.write(yaml.dump([d], allow_unicode=True, default_flow_style=False, sort_keys=False, indent=4))
            yaml_file.write('\n')
    
    return op


def get_text_box(display_message="Enter text:", font=("Arial", 9, "bold")):
    def get_text():
        entered_text = text_entry.get()
        root.destroy()  # Close the window after getting the text
        return entered_text
    
    root = tk.Tk()
    root.title("Text Input")
    
    # Display message
    label = tk.Label(root, text=display_message, font=font)
    label.pack()
    
    # Text Entry
    text_entry = tk.Entry(root, width=30)
    text_entry.pack()
    
    # Button
    button = tk.Button(root, text="Submit", command=lambda: result.set(get_text()))
    button.pack()
    
    result = tk.StringVar()
    result.set("")  # Initializing the result
    
    root.mainloop()
    
    if result.get()=='':
        return 'form_diff_op.html'  
    else:
        return result.get()
    

try:

    show_message('''
        PyXComparer (May2024 Version:1.0)        
    ___________________________________
                
    This tool is designed to simplify the process of monitoring changes between different versions of ODK XLSForms. 

    Follow the steps below to get started:

    Select Old Version: 
                First you select the older version of the XLSForm file (Form 1).

    Select Newer Version: 
                When prompted to select the file again, select the newer version of the XLSForm 
                file that you wish to compare with Form 1.

    Compare: 
                Once both versions are selected, automatically the 'Comparison' will be done.

    View Differences: 
                The differences between the two versions will be displayed in a separate window. 
                You can navigate through the changes to review them.

    Save HTML Report: 
                After reviewing the differences, you will be prompted to save an HTML report file. 
                Enter the desired filename and click "Save" to save the report.
    ______________________________________
                
    PyXComparer will generate a human-readable HTML report summarizing the changes between the two versions of the
    XLSForms, helping you to easily track modifications and updates.
                
    YAML data dictionaries for the forms will also be generated
    ______________________________________

    Thank you for using PyXComparer! 
                
    If you have any questions or feedback, feel free to reach out to me on joybindroo@gmail.com.
    ______________________________________             
                ''',font=("Arial", 8))

    show_message('Select Old Version of XLSForm (.xlsx)')
    xf1 = get_file_path()
    print('>>Read: ',xf1)
    show_message('Select New Version of XLSForm (.xlsx)')
    xf2 = get_file_path()
    print('>>Read: ',xf1)

    yf1 = xf1.replace('.','_')+'.yaml'
    yf2 = xf2.replace('.','_')+'.yaml'

    xlsxSurvey_to_Yaml(xf1,yf1)
    print('>>Converted Form1: ',yf1)
    xlsxSurvey_to_Yaml(xf2,yf2)
    print('>>Converted Form2: ',yf1)

    
    txt1=read_text_file(yf1)
    txt2=read_text_file(yf2)
    show_diff(txt1, txt2)
    fname=get_text_box('Enter output filename without extension and full path.')+'.html'
    generate_diff_report(txt1, txt2, fname)
    show_message( '''File Saved Successfully on Disk. Click OK to exit.''')
    

except Exception as e:
    show_message(f"An error occurred: {str(e)}")

