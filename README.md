# NicoCourts.com Administrator Interface

Originally I was trying to do the adminstrator interface all in Angular, but it ends up that TypeScript is really just not suited to the kind of computing I wanted to do.

Thus I went to the old standby -- Python. I found a great package `pywebview` that is a great wrapper for a GTK+ webview window. That allows me to design the interface in HTML/CSS/Javascript while being able to do all the computation behind the scenes in Python.

At the moment the interface is pretty barren. I have written some methods to interact with the API, so now I just need to get the UI where I want it.
