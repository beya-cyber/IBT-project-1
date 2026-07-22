history_stack = []

# Push actions
history_stack.append("Deposit: 500 ETB")
history_stack.append("Withdraw: 200 ETB")
history_stack.append("Transfer: 100 ETB")

# Pop newest action
last_action = history_stack.pop()
print(f"Popped newest action: {last_action}")
print(f"Remaining history: {history_stack}")


# 2. Queue Implementation (FIFO for Fair Transfer Processing)
print("\n--- 2. Pending Transfers Queue ---")
transfer_queue = deque()

# Enqueue transfers
transfer_queue.append({"from": "ACC1", "to": "ACC2", "amount": 300})
transfer_queue.append({"from": "ACC3", "to": "ACC1", "amount": 150})

# Dequeue oldest transfer
next_transfer = transfer_queue.popleft()
print(f"Processed transfer: {next_transfer}")
print(f"Remaining queued transfers: {list(transfer_queue)}")


# 3. Account Registry Dictionary (O(1) Lookup)
print("\n--- 3. Account Registry Dict ---")
registry = {
    "CBE-1001": {"owner": "Almaz", "balance": 1500},
    "CBE-1002": {"owner": "Dawit", "balance": 700}
}

# O(1) Lookup
acc_num = "CBE-1001"
print(f"Fast lookup for {acc_num}: {registry.get(acc_num)}")