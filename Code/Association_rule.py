# Association rule
#from mlxtend.frequent_patterns import apriori
import tkinter as tk
from matplotlib import pyplot
from mpl_toolkits.mplot3d import Axes3D
from tkinter import *
from tkinter import filedialog, messagebox, ttk
#import numpy as np
import matplotlib.pyplot as plt
import pandas as pd
import random

# initalise tkinter
root = tk.Tk()
root.title("Association Rule")
# set the root dimensions
root.geometry("500x450")  
# tells the root to not let the widgets inside it determine its size.
root.pack_propagate(False)
# makes the root window fixed in size.
root.resizable(0, 0)  

# declaration 
support_var = tk.DoubleVar()
confidence_var = tk.DoubleVar()
lift_var = tk.DoubleVar()

# Frame for Description
result_frame = tk.LabelFrame(root, text="Description")
result_frame.place(height=100, width=500, rely=0.75, relx=0)

# Frame for open data file
file_frame = tk.LabelFrame(root, text="Open Data File")
file_frame.place(height=100, width=500, rely=0.35, relx=0)

# Create Text Boxes Labels
min_support_label = Label(root, text="Min support").grid(row=0, column=0)
min_confidence_Label = Label(root, text="Min confidence").grid(row=1, column=0)
min_lift_Label = Label(root, text="Min lift").grid(row=2, column=0)

# Create Text Boxes
min_support = Entry(root, textvariable=support_var).grid(row=0, column=1)
min_confidence = Entry(root, textvariable=confidence_var).grid(row=1, column=1)
min_lift = Entry(root, textvariable=lift_var).grid(row=2, column=1)

# Buttons
button1 = tk.Button(file_frame, text="Browse A Data File",
                    command=lambda: File_dialog())
button1.place(rely=0.65, relx=0.50)

button2 = tk.Button(file_frame, text="Visualization",
                    command=lambda: Load_excel_data())
button2.place(rely=0.65, relx=0.30)

# file path text
label_file = ttk.Label(file_frame, text="No File Selected")
label_file.place(rely=0, relx=0)

# Result text
label_result = ttk.Label(
    result_frame, text="For testing you can use data Market_Basket_Optimisation.csv \r\n with 0.003 min support, 0.2 min confidence and 3 min lift. " )

label_result.place(rely=0, relx=0)


def File_dialog():
    """This Function will open the file explorer"""
    filename = filedialog.askopenfilename(initialdir="/",
                                          title="Select A File",
                                          filetype=(("csv files", "*.csv"), ("All Files", "*.*")))
    label_file["text"] = filename
    return None

def Load_excel_data():

    support = support_var.get()
    confidence = confidence_var.get()
    lift = lift_var.get()
    try:
        if lift<=1:        
            print("min lift must be biger than 1.")
            label_result["text"] = "min lift must be biger than 1."             
    except ValueError:
        tk.messagebox.showerror(
            "Information", "The value you have chosen is invalid,min lift must be biger than 1.")     
# Data Preprocessing
    file_path = label_file["text"]
    try:
        excel_filename = r"{}".format(file_path)
        df = pd.read_csv(excel_filename, header=None)

    except ValueError:
        tk.messagebox.showerror(
            "Information", "The file you have chosen is invalid")
        return None
    except FileNotFoundError:
        tk.messagebox.showerror("Information", f"No such file as {file_path}")
        return None
    
    transactions = []
    for i in range(0, df.index[-1]+1):
        transactions.append([str(df.values[i,j]) for j in range(0, 20)])
    
    # Training the Apriori model on the dataset
    from apyori import apriori
    rules = apriori(transactions, min_support = support, min_confidence = confidence, min_lift = lift)
    
    # Visualising the results    
    results = list(rules)   
    with open("resultfile.txt", "w") as f:
        s=[]  
        c=[]
        l=[]
        for item in results:    
            # first index of the inner list
            # Contains base item and add item
            pair = item[0] 
            items = [x for x in pair]
            f.write("Rule: " + items[0] + " -> " + items[1])
            f.write("\n")
            support=str(item[1])            
            confidence=str(item[2][0][2])
            lift=str(item[2][0][3])
            s.append(float(support))
            c.append(float(confidence))
            l.append(float(lift))
            #second index of the inner list
            f.write("Support: " + support)
            f.write("\n")
            #third index of the list located at 0th
            #of the third index of the inner list        
            f.write("Confidence: " + confidence)
            f.write("\n")
            f.write("Lift: " + str(item[2][0][3]))
            f.write("\n")
            f.write("=====================================")
            f.write("\n")
    # the python code to build scatter plot.           
        plt.scatter(s, c, alpha=0.6,marker='o')
    plt.title('Association Rules')
    plt.xlabel('support')
    plt.ylabel('confidence')
    plt.show()
    # Since few points here have the same values I added small random values to show all points.
    for i in range (len(s)):
       s[i] = s[i] + 0.0025 * (random.randint(1,10) - 5) 
       c[i] = c[i] + 0.0025 * (random.randint(1,10) - 5)        
       rgb = (random.random(), random.random(), random.random())          
       plt.scatter(s, c, alpha=0.6,marker='o', c=[rgb])
    plt.title('Association Rules with small random values')
    plt.xlabel('support')
    plt.ylabel('confidence')
    plt.show()    
    # Plotting 3D plot for support confidence lift.  
    fig = plt.figure()
    ax = fig.add_subplot(111, projection = "3d")
    ax.scatter(s, c, l)
    ax.set_xlabel("Support")
    ax.set_ylabel("Confidence")
    ax.set_zlabel("lift") 
    plt.show() 
    # open the result file and write it.
    f=open("resultfile.txt", "r")
    print(f.read())
    # result text
    label_result["text"] = "Visualization completed and The result sent into a file in your path."

root.mainloop()
