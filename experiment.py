import time
import statistics
import matplotlib.pyplot as plt
import math
from redblacktrees import RedBlackTree
from typing import Optional, TypeVar

T = TypeVar("T")

class NaiveBST[T]:
    value: T
    left: Optional["NaiveBST[T]"]
    right: Optional["NaiveBST[T]"]
    
    def __init__(self, value: T):
        self.value = value
        self.left = None
        self.right = None
    
    @staticmethod
    def fromList(xs: list[T]) -> Optional["NaiveBST[T]"]:
        if len(xs) == 0:
            return None
        tree = NaiveBST(xs[0])
        for x in xs[1:]:
            tree.insert(x)
        return tree
    
    def insert(self, x: T):
        cur = self
        while True:
            if x < cur.value:
                if cur.left is None:
                    cur.left = NaiveBST(x)
                    return
                else:
                    cur = cur.left
            elif x > cur.value:
                if cur.right is None:
                    cur.right = NaiveBST(x)
                    return
                else:
                    cur = cur.right
            else:
                raise RuntimeError("Duplicate key insertion is not allowed")
    
    def contains(self, x: T) -> bool:
        cur: Optional["NaiveBST[T]"] = self
        while cur is not None:
            if x < cur.value:
                cur = cur.left
            elif x > cur.value:
                cur = cur.right
            else:
                return True
        return False

def time_contains(tree, value, repeats=50):
    times = []
    for _ in range(repeats):
        start = time.perf_counter()
        tree.contains(value)
        times.append(time.perf_counter() - start)
    return statistics.mean(times)

def time_insert_single(TreeClass, data, repeats=1):
    times = []
    for _ in range(repeats):
        start = time.perf_counter()
        tree = TreeClass.fromList(data)
        elapsed = time.perf_counter() - start
        times.append(elapsed / len(data))
    return statistics.mean(times)

def run_experiment():
    sizes = [5000, 10000, 20000, 40000, 80000]
    bst_contains_times = []
    rbt_contains_times = []
    bst_insert_times = []
    rbt_insert_times = []
    
    for n in sizes:
        print(f"n = {n}")
        data = list(range(n))
        
        bst = NaiveBST.fromList(data)
        rbt = RedBlackTree.fromList(data)
        
        target = n - 1
        bst_cont = time_contains(bst, target)
        rbt_cont = time_contains(rbt, target)
        bst_contains_times.append(bst_cont)
        rbt_contains_times.append(rbt_cont)
        
        bst_ins = time_insert_single(NaiveBST, data)
        rbt_ins = time_insert_single(RedBlackTree, data)
        bst_insert_times.append(bst_ins)
        rbt_insert_times.append(rbt_ins)
        
        print(f"BST contains: {bst_cont*1e6:.2f} us")
        print(f"RBT contains: {rbt_cont*1e6:.2f} us")
        print(f"BST insert: {bst_ins*1e6:.2f} us")
        print(f"RBT insert: {rbt_ins*1e6:.2f} us")
        print()
    
    # Theoretical complexity curves
    theo_linear_cont = [bst_contains_times[0] * (n / sizes[0]) for n in sizes]
    theo_log_cont = [rbt_contains_times[0] * (math.log2(n) / math.log2(sizes[0])) for n in sizes]
    theo_linear_ins = [bst_insert_times[0] * (n / sizes[0]) for n in sizes]
    theo_log_ins = [rbt_insert_times[0] * (math.log2(n) / math.log2(sizes[0])) for n in sizes]
    
    # Creating plots
    fig, ((ax1, ax2), (ax3, ax4)) = plt.subplots(2, 2, figsize=(14, 10))
    
    # Plot 1: contains absolute times
    ax1.plot(sizes, [t*1e6 for t in bst_contains_times], 'o-', label="Naive BST")
    ax1.plot(sizes, [t*1e6 for t in rbt_contains_times], 's-', label="Red-Black Tree")
    ax1.plot(sizes, [t*1e6 for t in theo_linear_cont], '--', alpha=0.5, label="O(n)")
    ax1.plot(sizes, [t*1e6 for t in theo_log_cont], '--', alpha=0.5, label="O(log n)")
    ax1.set_xlabel("n")
    ax1.set_ylabel("Time (microseconds)")
    ax1.set_title("contains Performance")
    ax1.legend()
    ax1.grid(True)
    
    # Plot 2: contains speedup
    speedup_cont = [bst / rbt for bst, rbt in zip(bst_contains_times, rbt_contains_times)]
    ax2.plot(sizes, speedup_cont, 'o-')
    ax2.set_xlabel("n")
    ax2.set_ylabel("Speedup (BST/RBT)")
    ax2.set_title("contains Speedup")
    ax2.grid(True)
    
    # Plot 3: insert absolute times
    ax3.plot(sizes, [t*1e6 for t in bst_insert_times], 'o-', label="Naive BST")
    ax3.plot(sizes, [t*1e6 for t in rbt_insert_times], 's-', label="Red-Black Tree")
    ax3.plot(sizes, [t*1e6 for t in theo_linear_ins], '--', alpha=0.5, label="O(n)")
    ax3.plot(sizes, [t*1e6 for t in theo_log_ins], '--', alpha=0.5, label="O(log n)")
    ax3.set_xlabel("n")
    ax3.set_ylabel("Time (microseconds)")
    ax3.set_title("insert Performance")
    ax3.legend()
    ax3.grid(True)
    
    # Plot 4: insert speedup
    speedup_ins = [bst / rbt for bst, rbt in zip(bst_insert_times, rbt_insert_times)]
    ax4.plot(sizes, speedup_ins, 'o-')
    ax4.set_xlabel("n")
    ax4.set_ylabel("Speedup (BST/RBT)")
    ax4.set_title("insert Speedup")
    ax4.grid(True)
    
    plt.tight_layout()
    plt.savefig("results.png")
    print("Saved to results.png")
    plt.show()

if __name__ == "__main__":
    run_experiment()


