# Make it run from the examples directory
import sys
sys.path.append("../liquer")

from liquer import *
import pandas as pd
import numpy as np
from time import sleep

@first_command(volatile=True)
def hello():
    return "Hello"


@first_command
def harmonic(n=100):
    a = np.linspace(0,2*np.pi,n)
    segment = np.array(a*10/(2*np.pi),dtype=int)
    return pd.DataFrame(
        dict(
            a=a,
            x=np.sin(a),
            y=np.cos(a),
            x2=np.sin(2*a),
            y2=np.cos(2*a),
            x3=np.sin(3*a),
            y3=np.cos(3*a),
            x4=np.sin(4*a),
            y4=np.cos(4*a),
            segment=segment,
            label=[f"{i+1}/{n}" for i in range(n)]
        )
    )

@command
def noise(df, sigma=0.1):
    columns = [c for c in df.columns if c.startswith("x") or c.startswith("y")]
    for c in columns:
        noise = np.random.normal(0.0,sigma,len(df))
        df[c]+=noise
    return df

@first_command
def start(count=5, context=None):
    for i in range(count):
        print(i)
        context.progress(i+1, count, message=f"Step {i+1} out of {count}")
        sleep(0.1)
    return f"Done {count}"


@first_command
def start2(count1=10, count2=10, context=None):
    from time import sleep

    p1 = context.new_progress_indicator() # low level progress reporting - create progress report handle
    p3 = context.new_progress_indicator()
    for i in range(count1):
        context.progress(
            i, count1, message=f"Outer loop {i} out of {count1}", identifier=p1
        ) # do the report with the andle
        p2 = context.new_progress_indicator()
        context.info(f"Step {i} started")
        for j in range(count2):
            print(i, j)
            context.progress(
                j, count2, message=f"Inner loop {j} out of {count2}", identifier=p2
            )
            context.progress(j, message=f"Undifferentiated {j}", identifier=p3)
            sleep(0.1)
        context.info(f"Step {i} finished")
        context.remove_progress_indicator(p2)
    context.remove_progress_indicator(p1) #remove the handle after use
    context.remove_progress_indicator(p3) #remove the handle after use

    return f"Done {count1}x{count2}"


@command
def nested(x, count1=5, count2=5, context=None):
    context.info("Nested command")
    text = "Nested: "+str(x)+"\n"
    for i in context.progress_iter(range(count1)):
        context.info(f"Nested command iteration {i}")
        text += str(context.evaluate(f"start-{count2+i}").get())+"\n"
        context.set_html_preview(f"""
        <h1>Nested command</h1>
        <pre>{text}</pre
        """)
    return text

@first_command
def recursive(count=5, context=None):
    context.info(f"Recursive command {count}")
    if count>0:
        text=""
        x = str(context.evaluate(f"recursive-{count-1}").get())+"\n"
        for i in context.progress_iter(range(count), True):
            text += x
            sleep(0.1)
            context.set_html_preview(f"""
            <h1>Nested command</h1>
            <pre>{text}</pre
            """)
        text+="\n"
    else:
        return "*"
    return text

