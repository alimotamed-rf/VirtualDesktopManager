from pywinauto import Desktop


print("Outlook UI test")
print("-" * 50)


windows = Desktop(backend="uia").windows()


for w in windows:

    title = w.window_text()


    if "Outlook" in title:

        print("FOUND WINDOW:")
        print(title)

        print()
        print("Children:")
        print("-" * 50)


        try:

            for child in w.descendants():

                text = child.window_text()


                if text:

                    print(
                        type(child).__name__,
                        ":",
                        text
                    )


        except Exception as e:

            print(e)