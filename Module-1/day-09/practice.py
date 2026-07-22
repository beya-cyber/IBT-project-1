# --- 1. Tree: Branch Hierarchy ---
class Branch:
    def __init__(self, name, balance=0):
        self.name = name
        self.balance = balance
        self.sub_branches = []

    def add_sub_branch(self, branch):
        self.sub_branches.append(branch)

    # Recursive total balance across the hierarchy
    def total_balance(self):
        total = self.balance
        for child in self.sub_branches:
            total += child.total_balance()
        return total


# --- 2. Graph: Transfer Network ---
class TransferNetwork:
    def __init__(self):
        self.graph = {}

    def add_transfer(self, sender, receiver):
        if sender not in self.graph:
            self.graph[sender] = []
        self.graph[sender].append(receiver)

    # Breadth-First Search (BFS)
    def bfs(self, start_account):
        visited = set([start_account])
        queue = deque([start_account])
        reachable = []

        while queue:
            current = queue.popleft()
            for neighbor in self.graph.get(current, []):
                if neighbor not in visited:
                    visited.add(neighbor)
                    queue.append(neighbor)
                    reachable.append(neighbor)
        return reachable


# --- 3. Execution & Testing ---
if __name__ == "__main__":
    # --- Tree Setup ---
    head_office = Branch("Head Office (Addis Ababa)", 100000)
    region_north = Branch("Northern Region", 50000)
    region_south = Branch("Southern Region", 40000)

    branch_mekelle = Branch("Mekelle Branch", 20000)
    branch_hawassa = Branch("Hawassa Branch", 15000)

    # Build hierarchy
    head_office.add_sub_branch(region_north)
    head_office.add_sub_branch(region_south)
    region_north.add_sub_branch(branch_mekelle)
    region_south.add_sub_branch(branch_hawassa)

    print("--- Tree: Bank Total Balance ---")
    print(f"Total Bank System Balance: {head_office.total_balance():,} ETB")

    # --- Graph Setup ---
    network = TransferNetwork()
    network.add_transfer("CBE-1", "CBE-2")
    network.add_transfer("CBE-1", "CBE-3")
    network.add_transfer("CBE-2", "CBE-4")
    network.add_transfer("CBE-3", "CBE-5")

    print("\n--- Graph: BFS Reachable Accounts from CBE-1 ---")
    reachable = network.bfs("CBE-1")
    print(f"Accounts reachable from CBE-1: {reachable}")