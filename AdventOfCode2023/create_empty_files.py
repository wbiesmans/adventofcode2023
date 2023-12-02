if __name__  == "__main__":
    person = "Wouter"
    days = range(2, 5)
    extension = ".py"

    for day in days:
        # create empty python files
        with open(f"{person}\day_{day}_part_1{extension}", "w") as f:
            pass
        with open(f"{person}\day_{day}_part_2{extension}", "w") as f:
            pass

        # create empty input files
        with open(f"{person}\day_{day}_input_1.txt", "w") as f:
            pass
        with open(f"{person}\day_{day}_input_2.txt", "w") as f:
            pass
        with open(f"{person}\day_{day}_input_final.txt", "w") as f:
            pass