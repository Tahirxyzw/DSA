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
                raise RuntimeError("Duplicate key insertion is not allowed.")
    
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

def time_contains(tree, value, repeats=50):  # Reduced from 100
    times = []
    for _ in range(repeats):
        start = time.perf_counter()
        tree.contains(value)
        times.append(time.perf_counter() - start)
    return statistics.mean(times)

def time_insert_single(TreeClass, data, repeats=1):  # Reduced from 3
    times = []
    for _ in range(repeats):
        start = time.perf_counter()
        tree = TreeClass.fromList(data)
        elapsed = time.perf_counter() - start
        times.append(elapsed / len(data))
    return statistics.mean(times)

def run_experiment():
    # Reduced sizes - still shows the trend clearly
    sizes = [5_000, 10_000, 20_000, 40_000, 80_000]  # Removed 160k
    bst_contains_times = []
    rbt_contains_times = []
    bst_insert_times = []
    rbt_insert_times = []
    
    for n in sizes:
        print(f"Testing n = {n:,}")
        data = list(range(n))
        
        # Build trees
        bst = NaiveBST.fromList(data)
        rbt = RedBlackTree.fromList(data)
        
        # Test contains
        target = n - 1
        bst_cont = time_contains(bst, target, repeats=50)
        rbt_cont = time_contains(rbt, target, repeats=50)
        bst_contains_times.append(bst_cont)
        rbt_contains_times.append(rbt_cont)
        
        # Test insert
        bst_ins = time_insert_single(NaiveBST, data, repeats=1)
        rbt_ins = time_insert_single(RedBlackTree, data, repeats=1)
        bst_insert_times.append(bst_ins)
        rbt_insert_times.append(rbt_ins)
        
        print(f"  Contains - BST: {bst_cont*1e6:.2f} μs, RBT: {rbt_cont*1e6:.2f} μs")
        print(f"  Insert   - BST: {bst_ins*1e6:.2f} μs, RBT: {rbt_ins*1e6:.2f} μs\n")
    
    # Calculate theoretical curves
    theo_linear_cont = [bst_contains_times[0] * (n / sizes[0]) for n in sizes]
    theo_log_cont = [rbt_contains_times[0] * (math.log2(n) / math.log2(sizes[0])) for n in sizes]
    theo_linear_ins = [bst_insert_times[0] * (n / sizes[0]) for n in sizes]
    theo_log_ins = [rbt_insert_times[0] * (math.log2(n) / math.log2(sizes[0])) for n in sizes]
    
    # Plot results
    fig, ((ax1, ax2), (ax3, ax4)) = plt.subplots(2, 2, figsize=(16, 12))
    
    # contains() Absolute Times
    ax1.plot(sizes, [t*1e6 for t in bst_contains_times], marker="o", linewidth=2.5, markersize=8, label="Naive BST", color='#2E86AB')
    ax1.plot(sizes, [t*1e6 for t in rbt_contains_times], marker="s", linewidth=2.5, markersize=8, label="Red-Black Tree", color='#A23B72')
    ax1.plot(sizes, [t*1e6 for t in theo_linear_cont], linestyle="--", linewidth=2, alpha=0.6, label="O(n)", color='#2E86AB')
    ax1.plot(sizes, [t*1e6 for t in theo_log_cont], linestyle="--", linewidth=2, alpha=0.6, label="O(log n)", color='#A23B72')
    ax1.set_xlabel("Number of elements (n)", fontsize=12, fontweight='bold')
    ax1.set_ylabel("Average contains() time (μs)", fontsize=12, fontweight='bold')
    ax1.set_title("contains() Performance: Absolute Times", fontsize=14, fontweight="bold", pad=15)
    ax1.legend(fontsize=10)
    ax1.grid(True, alpha=0.3)
    
    # contains() Speedup
    speedups_cont = [bst / rbt for bst, rbt in zip(bst_contains_times, rbt_contains_times)]
    ax2.plot(sizes, speedups_cont, marker="o", linewidth=2.5, markersize=8, color='#F18F01')
    ax2.set_xlabel("Number of elements (n)", fontsize=12, fontweight='bold')
    ax2.set_ylabel("Speedup factor", fontsize=12, fontweight='bold')
    ax2.set_title("contains() Speedup: RBT vs Naive BST", fontsize=14, fontweight="bold", pad=15)
    ax2.grid(True, alpha=0.3)
    
    # insert() Absolute Times
    ax3.plot(sizes, [t*1e6 for t in bst_insert_times], marker="o", linewidth=2.5, markersize=8, label="Naive BST", color='#2E86AB')
    ax3.plot(sizes, [t*1e6 for t in rbt_insert_times], marker="s", linewidth=2.5, markersize=8, label="Red-Black Tree", color='#A23B72')
    ax3.plot(sizes, [t*1e6 for t in theo_linear_ins], linestyle="--", linewidth=2, alpha=0.6, label="O(n)", color='#2E86AB')
    ax3.plot(sizes, [t*1e6 for t in theo_log_ins], linestyle="--", linewidth=2, alpha=0.6, label="O(log n)", color='#A23B72')
    ax3.set_xlabel("Number of elements (n)", fontsize=12, fontweight='bold')
    ax3.set_ylabel("Average insert() time (μs)", fontsize=12, fontweight='bold')
    ax3.set_title("insert() Performance: Absolute Times", fontsize=14, fontweight="bold", pad=15)
    ax3.legend(fontsize=10)
    ax3.grid(True, alpha=0.3)
    
    # insert() Speedup
    speedups_ins = [bst / rbt for bst, rbt in zip(bst_insert_times, rbt_insert_times)]
    ax4.plot(sizes, speedups_ins, marker="o", linewidth=2.5, markersize=8, color='#F18F01')
    ax4.set_xlabel("Number of elements (n)", fontsize=12, fontweight='bold')
    ax4.set_ylabel("Speedup factor", fontsize=12, fontweight='bold')
    ax4.set_title("insert() Speedup: RBT vs Naive BST", fontsize=14, fontweight="bold", pad=15)
    ax4.grid(True, alpha=0.3)
    
    plt.tight_layout(pad=3.0)
    plt.savefig("performance_analysis.png", dpi=300, bbox_inches="tight")
    print("Results saved to 'performance_analysis.png'")
    plt.show()

if __name__ == "__main__":
    run_experiment()