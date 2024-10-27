from collections import Counter

def post_process(output):
    element_counts = Counter(item[4] for item in output)    
    result = [[cls,count] for cls, count in element_counts.items()]
    return result

if __name__ == "__main__":
    # Example output list with different classes
    output = [
        [370, 210, 457, 322, 'horse', 0.6741992831230164],
        [227, 196, 420, 364, 'horse', 0.8214676976203918],
        [0, 186, 154, 287, 'cow', 0.8605173826217651],
        [433, 213, 595, 347, 'horse', 0.9438263177871704],
        [0, 192, 315, 411, 'cow', 0.95638507604599]
    ]

    # Call the function and print the result
    result = post_process(output)
    print(result)
