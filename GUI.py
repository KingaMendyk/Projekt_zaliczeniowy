import tkinter as tk
import tkinter.ttk as ttk
from tkinter import filedialog
from tkinter.filedialog import asksaveasfile
from screeninfo import get_monitors
import pickle
import os
import dbsql
import model
import matplotlib
import matplotlib.pyplot as plt
matplotlib.use('TkAgg')


class GUI(tk.Tk):
    def __init__(self):
        super().__init__()
        self.db = dbsql.DbSQL("wine_database.db", "wine.data")
        self.model = model.Model(self.db)

        self.screen_width = get_monitors()[0].width
        self.screen_height = get_monitors()[0].height

        self.title("Wine recognition model")
        self.iconphoto(True, tk.PhotoImage(file=r"images/wine_icon.png"))
        self.geometry(f"{int(self.screen_width / 2)}x{int(self.screen_height / 2)}")

        question_frame = tk.Frame(self)
        question_frame.pack(side="bottom", fill="y", expand=True)
        question_label = tk.Label(question_frame, text="What would you like to do?", font=("Arial", 15))
        question_label.pack(pady=10)

        train_button = tk.Button(question_frame, text="Train", font=("Arial", 12), command=self.train_window)
        test_button = tk.Button(question_frame, text="Test", font=("Arial", 12), command=self.test_window)
        predict_button = tk.Button(question_frame, text="Predict", font=("Arial", 12), command=self.predict_window)
        add_button = tk.Button(question_frame, text="Add new data", font=("Arial", 12), command=self.add_window)
        rebuild_button = tk.Button(question_frame, text="Rebuild model", font=("Arial", 12),
                                   command=self.rebuild_window)
        table_button = tk.Button(question_frame, text="View table", font=("Arial", 12), command=self.table_window)
        graph_button = tk.Button(question_frame, text="View graph", font=("Arial", 12), command=self.graph_window)
        save_button = tk.Button(question_frame, text="Save model", font=("Arial", 12), command=self.save_window)
        read_button = tk.Button(question_frame, text="Read model", font=("Arial", 12), command=self.read_window)

        train_button.pack(side="left", anchor="n", padx=5)
        test_button.pack(side="left", anchor="n", padx=5)
        predict_button.pack(side="left", anchor="n", padx=5)
        add_button.pack(side="left", anchor="n", padx=5)
        rebuild_button.pack(side="left", anchor="n", padx=5)
        table_button.pack(side="left", anchor="n", padx=5)
        graph_button.pack(side="left", anchor="n", padx=5)
        save_button.pack(side="left", anchor="n", padx=5)
        read_button.pack(side="left", anchor="n", padx=5)

        title_frame = tk.Frame(self, borderwidth=2, relief="ridge")
        title_frame.pack(side="left", anchor="n", padx=10, pady=10, fill="x", expand=True)
        title_label = tk.Label(title_frame, text="🍇 Welcome to wine database 🍇", font=("Helvetica", 30))
        title_label.pack()

        info_icon = tk.PhotoImage(file=r"images/info_icon.png")
        info_button = tk.Button(self, text="info", image=info_icon, command=self.info_window)
        info_button.pack(side="right", anchor="nw", padx=5, pady=15)

        self.mainloop()

    def info_window(self):
        window = tk.Toplevel(self)
        window.title("Dataset info")
        file = "wine.names"
        scroll = tk.Scrollbar(window, orient="vertical")
        scroll.pack(side="right", fill="y")

        text = tk.Text(window, yscrollcommand=scroll.set)
        with open(file) as file_object:
            for line in file_object:
                text.insert("end", line)

        scroll.config(command=text.yview)
        text.configure(state="disabled")
        text.pack()
        close_button = tk.Button(window, text="Close", command=window.destroy)
        close_button.pack(pady=5)

    def table_window(self):
        window = tk.Toplevel(self)
        window.title("Table view")
        window.geometry(f"{int(self.screen_width / 1.5)}x{int(self.screen_height / 2)}")

        scroll = tk.Scrollbar(window, orient="vertical")
        scroll.pack(side="right", fill="y")

        treeview = ttk.Treeview(window, yscrollcommand=scroll.set)
        treeview["columns"] = ("alcohol", "malic_acid", "ash", "alcalinity_of_ash", "magnesium",
                               "total_phenols", "flavanoids", "nonflavanoid_phenols", "proanthocyanins",
                               "color_intensity", "hue", "diluted", "proline", "category")

        treeview.column("#0", width=0)
        treeview.heading("alcohol", text="Alcohol")
        treeview.heading("malic_acid", text="Malic acid")
        treeview.heading("ash", text="Ash")
        treeview.heading("alcalinity_of_ash", text="Alcalinity of ash")
        treeview.heading("magnesium", text="Magnesium")
        treeview.heading("total_phenols", text="Total phenols")
        treeview.heading("flavanoids", text="Flavanoids")
        treeview.heading("nonflavanoid_phenols", text="Nonflavanoid phenols")
        treeview.heading("proanthocyanins", text="Proanthocyanins")
        treeview.heading("color_intensity", text="Color intensity")
        treeview.heading("hue", text="Hue")
        treeview.heading("diluted", text="OD280/OD315 of diluted wines")
        treeview.heading("proline", text="Proline")
        treeview.heading("category", text="Category")

        for col in treeview["columns"]:
            treeview.column(col, width=90)

        scroll.config(command=treeview.yview)
        treeview.pack(fill="both", expand=True)
        data = self.db.fetch_data()
        treeview.delete(*treeview.get_children())
        for row in data:
            d = list()
            for i in range(len(row)):
                d.append(row[i])
            treeview.insert("", "end", values=tuple(d))

    def graph_window(self):
        data = self.db.fetch_data()
        dataset = {}
        for i in range(len(data)):
            item = data[i]
            key = item[-1]
            if key not in dataset.keys():
                dataset[key] = 1
            else:
                dataset[key] = dataset[key] + 1

        keys = list(dataset.keys())
        values = list(dataset.values())

        plt.bar(keys, values, width=0.4)
        plt.xlabel("Category")
        plt.ylabel("Count")
        plt.title("Number of instances per category")
        plt.show()

    def add_window(self):
        window = tk.Toplevel(self)
        window.title("Add new item")

        alcohol_label = tk.Label(window, text="Alcohol:")
        alcohol_label.pack()
        alcohol_entry = tk.Entry(window)
        alcohol_entry.pack()

        malic_acid_label = tk.Label(window, text="Malic Acid:")
        malic_acid_label.pack()
        malic_acid_entry = tk.Entry(window)
        malic_acid_entry.pack()

        ash_label = tk.Label(window, text="Ash:")
        ash_label.pack()
        ash_entry = tk.Entry(window)
        ash_entry.pack()

        alcalinity_of_ash_label = tk.Label(window, text="Alcalinity of ash:")
        alcalinity_of_ash_label.pack()
        alcalinity_of_ash_entry = tk.Entry(window)
        alcalinity_of_ash_entry.pack()

        magnesium_label = tk.Label(window, text="Magnesium:")
        magnesium_label.pack()
        magnesium_entry = tk.Entry(window)
        magnesium_entry.pack()

        total_phenols_label = tk.Label(window, text="Total phenols:")
        total_phenols_label.pack()
        total_phenols_entry = tk.Entry(window)
        total_phenols_entry.pack()

        flavanoids_label = tk.Label(window, text="Flavanoids:")
        flavanoids_label.pack()
        flavanoids_entry = tk.Entry(window)
        flavanoids_entry.pack()

        nonflavanoid_phenols_label = tk.Label(window, text="Nonflavanoid phenols:")
        nonflavanoid_phenols_label.pack()
        nonflavanoid_phenols_entry = tk.Entry(window)
        nonflavanoid_phenols_entry.pack()

        proanthocyanins_label = tk.Label(window, text="Proanthocyanins:")
        proanthocyanins_label.pack()
        proanthocyanins_entry = tk.Entry(window)
        proanthocyanins_entry.pack()

        color_intensity_label = tk.Label(window, text="Color intensity:")
        color_intensity_label.pack()
        color_intensity_entry = tk.Entry(window)
        color_intensity_entry.pack()

        hue_label = tk.Label(window, text="Hue:")
        hue_label.pack()
        hue_entry = tk.Entry(window)
        hue_entry.pack()

        diluted_label = tk.Label(window, text="OD280/OD315 of diluted wines:")
        diluted_label.pack()
        diluted_entry = tk.Entry(window)
        diluted_entry.pack()

        proline_label = tk.Label(window, text="Proline:")
        proline_label.pack()
        proline_entry = tk.Entry(window)
        proline_entry.pack()

        category_label = tk.Label(window, text="Category:")
        category_label.pack()
        category_entry = tk.Entry(window)
        category_entry.pack()

        def add_item():
            data = list()
            data.append(alcohol_entry.get())
            data.append(malic_acid_entry.get())
            data.append(ash_entry.get())
            data.append(alcalinity_of_ash_entry.get())
            data.append(magnesium_entry.get())
            data.append(total_phenols_entry.get())
            data.append(flavanoids_entry.get())
            data.append(nonflavanoid_phenols_entry.get())
            data.append(proanthocyanins_entry.get())
            data.append(color_intensity_entry.get())
            data.append(hue_entry.get())
            data.append(diluted_entry.get())
            data.append(proline_entry.get())
            data.append(category_entry.get())

            self.db.insert_data(data)
            self.model.refresh(self.db)
            window.destroy()

        add_button = tk.Button(window, text="Add", command=add_item)
        add_button.pack(pady=5)

    def test_window(self):
        ev_window = tk.Toplevel(self)
        ev_window.title("Testing")
        ev_window.geometry(f"{int(self.screen_width / 4)}x{int(self.screen_height / 2)}")
        ev_window.resizable(width=False, height=False)

        dummy_data = []
        data = []
        for i in range(13):
            data.append(0)
        dummy_data.append(data)

        p = self.model.predict(dummy_data)
        if p == "0":
            label = tk.Label(ev_window, text="Please train the model first!", font=("Arial", 15))
            label.pack(anchor="center")

        else:

            def ev(tset):
                acc = self.model.evaluate_accuracy(tset)
                matrix = self.model.evaluate_matrix(tset)
                report = self.model.evaluate_report(tset)

                acc_label.configure(text="Accuracy:\t" + str(acc))

                conf_matrix.delete(*conf_matrix.get_children())
                for row in range(matrix.shape[0]):
                    d = list()
                    for i in range(matrix.shape[1]):
                        d.append(matrix[row][i])
                    conf_matrix.insert("", "end", values=tuple(d))

                t_area.configure(state="normal")
                t_area.delete("1.0", "end")
                t_area.insert("end", report)
                t_area.configure(state="disabled")

            def change_to_test():
                button.configure(text="Train set", command=change_to_train)
                label.configure(text="Test set")
                ev("test")

            def change_to_train():
                button.configure(text="Test set", command=change_to_test)
                label.configure(text="Train set")
                ev("train")

            label = tk.Label(ev_window, text="Test set", font=("Arial", 15))
            label.pack(side="top", pady=5)

            button = tk.Button(ev_window, text="Train set", command=change_to_train)
            button.pack(side="top", anchor="e", padx=5)

            frame1 = tk.Frame(ev_window, borderwidth=4, relief="ridge", width=self.screen_width / 4,
                              height=self.screen_height / 6)

            frame2 = tk.Frame(ev_window, borderwidth=4, relief="ridge", width=frame1["width"],
                              height=frame1["height"])

            acc_label = tk.Label(frame1, text="Accuracy:\t")
            acc_label.pack(side="left")

            conf_matrix = ttk.Treeview(frame1)
            conf_matrix["columns"] = ("1", "2", "3")
            conf_matrix.column("#0", width=0)
            conf_matrix.heading("1", text="1")
            conf_matrix.heading("2", text="2")
            conf_matrix.heading("3", text="3")
            for col in conf_matrix["columns"]:
                conf_matrix.column(col, width=70)
            conf_matrix.pack(side="right")

            t_area = tk.Text(frame2)
            t_area.pack()

            frame1.pack(side="top", padx=10, pady=10, fill="both")
            frame2.pack(side="bottom", padx=10, pady=10, fill="both")
            ev("test")

    def train_window(self):
        window = tk.Toplevel(self)
        window.title("Train model")
        window.geometry(f"{int(self.screen_width / 8)}x{int(self.screen_height / 6)}")

        label = tk.Label(window, text="Split the data?")
        label.pack()

        def change_state0():
            slider.set(0)
            slider.configure(state="disabled")

        def change_state1():
            slider.configure(state="normal")

        radio_var = tk.IntVar(value=0)
        rb1 = tk.Radiobutton(window, text="no", variable=radio_var, value=0, command=change_state0)
        rb2 = tk.Radiobutton(window, text="yes", variable=radio_var, value=1, command=change_state1)
        rb1.pack()
        rb2.pack()

        label2 = tk.Label(window, text="Select test set size")
        label2.pack()
        slider = tk.Scale(window, from_=0, to=90, orient=tk.HORIZONTAL)
        slider.configure(state="disabled")
        slider.pack()

        def train():
            self.model.train(radio_var.get(), slider.get())
            ev_button.configure(state="normal")

        button_frame = tk.Frame(window)
        button_frame.pack(side="bottom", fill="y", expand=True)

        def evaluate():
            ev_window = tk.Toplevel(self)
            ev_window.title("Evaluation")
            ev_window.geometry(f"{int(self.screen_width / 2)}x{int(self.screen_height / 3)}")
            ev_window.resizable(width=False, height=False)

            res = self.model.evaluate_best("train")
            avg = res["avg"]
            param_grid = res["param_grid"]
            best_param = res["best_param"]
            best_score = res["best_score"]

            title_label = tk.Label(ev_window, text="Cross-validation score:")
            title_label.pack(side="top")

            def close():
                window.destroy()
                ev_window.destroy()

            close_button = tk.Button(ev_window, text="Close", command=close)
            close_button.pack(side="bottom", pady=5)

            lframe = tk.Frame(ev_window, borderwidth=4, relief="ridge", width=int(self.screen_width / 8),
                              height=int(self.screen_width / 4))
            lframe.pack(side="left", padx=10, pady=10, fill="both")
            avg_label = tk.Label(lframe, text="Average score:\t" + str(avg))
            avg_label.pack(padx=10, pady=10)
            param_label = tk.Label(lframe,
                                   text="Best parameters:\t" + str(best_param).replace("{", "").replace("}", ""))
            param_label.pack(padx=10, pady=10)
            score_label = tk.Label(lframe, text="Best score:\t" + str(best_score))
            score_label.pack(padx=10, pady=10)

            rframe = tk.Frame(ev_window, width=int(self.screen_width / 4), height=lframe["height"], borderwidth=4,
                              relief="ridge")
            rframe.pack(side="right", padx=10, pady=10, fill="both")
            t_area = tk.Text(rframe)
            t_area.insert("end", param_grid)
            t_area.configure(state="disabled")
            t_area.pack()

        button = tk.Button(button_frame, text="Train", command=train)
        ev_button = tk.Button(button_frame, text="Evaluate", command=evaluate)
        ev_button.configure(state="disabled")
        button.pack(side="left")
        ev_button.pack(side="right")

    def rebuild_window(self):
        self.model.rebuild(self.db)
        window = tk.Toplevel(self)
        window.title("Result")
        label = tk.Label(window, text="Success!", font=("Arial", 12))
        label.pack(anchor="center")

    def predict_window(self):
        window = tk.Toplevel(self)
        window.title("Predict new entry")

        alcohol_label = tk.Label(window, text="Alcohol:")
        alcohol_label.pack()
        alcohol_entry = tk.Entry(window)
        alcohol_entry.pack()

        malic_acid_label = tk.Label(window, text="Malic Acid:")
        malic_acid_label.pack()
        malic_acid_entry = tk.Entry(window)
        malic_acid_entry.pack()

        ash_label = tk.Label(window, text="Ash:")
        ash_label.pack()
        ash_entry = tk.Entry(window)
        ash_entry.pack()

        alcalinity_of_ash_label = tk.Label(window, text="Alcalinity of ash:")
        alcalinity_of_ash_label.pack()
        alcalinity_of_ash_entry = tk.Entry(window)
        alcalinity_of_ash_entry.pack()

        magnesium_label = tk.Label(window, text="Magnesium:")
        magnesium_label.pack()
        magnesium_entry = tk.Entry(window)
        magnesium_entry.pack()

        total_phenols_label = tk.Label(window, text="Total phenols:")
        total_phenols_label.pack()
        total_phenols_entry = tk.Entry(window)
        total_phenols_entry.pack()

        flavanoids_label = tk.Label(window, text="Flavanoids:")
        flavanoids_label.pack()
        flavanoids_entry = tk.Entry(window)
        flavanoids_entry.pack()

        nonflavanoid_phenols_label = tk.Label(window, text="Nonflavanoid phenols:")
        nonflavanoid_phenols_label.pack()
        nonflavanoid_phenols_entry = tk.Entry(window)
        nonflavanoid_phenols_entry.pack()

        proanthocyanins_label = tk.Label(window, text="Proanthocyanins:")
        proanthocyanins_label.pack()
        proanthocyanins_entry = tk.Entry(window)
        proanthocyanins_entry.pack()

        color_intensity_label = tk.Label(window, text="Color intensity:")
        color_intensity_label.pack()
        color_intensity_entry = tk.Entry(window)
        color_intensity_entry.pack()

        hue_label = tk.Label(window, text="Hue:")
        hue_label.pack()
        hue_entry = tk.Entry(window)
        hue_entry.pack()

        diluted_label = tk.Label(window, text="OD280/OD315 of diluted wines:")
        diluted_label.pack()
        diluted_entry = tk.Entry(window)
        diluted_entry.pack()

        proline_label = tk.Label(window, text="Proline:")
        proline_label.pack()
        proline_entry = tk.Entry(window)
        proline_entry.pack()

        prediction_label = tk.Label(window, text="Predicted category:\t", font=("Arial", 12))
        prediction_label.pack()

        def predict_item():
            listdata = []
            data = []
            data.append(alcohol_entry.get())
            data.append(malic_acid_entry.get())
            data.append(ash_entry.get())
            data.append(alcalinity_of_ash_entry.get())
            data.append(magnesium_entry.get())
            data.append(total_phenols_entry.get())
            data.append(flavanoids_entry.get())
            data.append(nonflavanoid_phenols_entry.get())
            data.append(proanthocyanins_entry.get())
            data.append(color_intensity_entry.get())
            data.append(hue_entry.get())
            data.append(diluted_entry.get())
            data.append(proline_entry.get())

            listdata.append(data)
            res = self.model.predict(listdata)

            if res == "0":
                prediction_label.configure(text="Please train the model first!")
            else:
                prediction_label.configure(text="Predicted category:\t" + res)

        pred_button = tk.Button(window, text="Predict", command=predict_item)
        pred_button.pack(pady=5)

    def save_window(self):
        files = [('All Files', '*.*'),
                 ('Python Files', '*.py'),
                 ('Text Document', '*.txt')]
        file = asksaveasfile(filetypes=files)

        if file is not None:
            with open(file.name, 'wb') as f:
                pickle.dump(self.model, f)
            file.close()

    def read_window(self):
        filename = filedialog.askopenfilename(initialdir="/", title="Select a File",
                                              filetypes=(("Text files", "*.txt*"), ("all files", "*.*")))
        if filename != "":
            with open(filename, 'rb') as file:
                readmodel = pickle.load(file)
                self.model = readmodel
