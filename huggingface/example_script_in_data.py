def main():
    import sys
    input = sys.stdin.read().split()
    ptr = 0
    T = int(input[ptr])
    ptr += 1
    for _ in range(T):
        R = int(input[ptr])
        ptr += 1
        A = list(map(int, input[ptr:ptr+2]))
        ptr += 2
        B = list(map(int, input[ptr:ptr+2]))
        ptr += 2
        C = list(map(int, input[ptr:ptr+2]))
        ptr += 2
        count = 0
        
        # Check Chef to Head Server
        dx = A[0] - B[0]
        dy = A[1] - B[1]
        if dx * dx + dy * dy <= R * R:
            count += 1
        
        # Check Head Server to Sous-Chef
        dx = B[0] - C[0]
        dy = B[1] - C[1]
        if dx * dx + dy * dy <= R * R:
            count += 1
        
        # Check Sous-Chef to Chef
        dx = C[0] - A[0]
        dy = C[1] - A[1]
        if dx * dx + dy * dy <= R * R:
            count += 1
        
        print("yes" if count >= 2 else "no")

main()