from pywinauto import Desktop


print("All active windows")
print("-" * 50)


windows = Desktop(backend="uia").windows()


for w in windows:

    title = w.window_text()

    if title:

        print(title)