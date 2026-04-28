
def print_decomposition_tree(edges):
    print("\nDECOMPOSITION TREE")
    print("------------------")

    for parent, child in edges:
        print(f"{parent} -> {child}")