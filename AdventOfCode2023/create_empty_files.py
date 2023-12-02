if __name__  == "__main__":
    person = "Wouter"  # Used as subfolder name
    days = range(2, 5) # Days to create files for. E.g. range(1, 26) for all days
    extension = ".py"

    for day in days:
        # create empty python files for each part
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