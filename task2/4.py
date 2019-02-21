def get_sum_of_points(inlist):
    round_points = []
    operation_counter = 1
    iround = 0

    for string in inlist:
        # string is +
        if string == '+':
            report = "Round {}: You could get {} + {} = {} points. The sum is: {}."
            print(report.format(
                iround+1, round_points[-1],
                round_points[-2], round_points[-1] + round_points[-2],
                sum(round_points)))
            round_points.append(round_points[-1] + round_points[-2])

        elif string == 'C':
            report = "Operation {}: The round {}'s" \
                     " data was invalid. The sum is: {}."
            operation_counter += 1
            iround -= 1
            round_points = round_points[:-1]
            print(report.format(operation_counter, iround+1, sum(round_points)))

        elif string == 'D':
            report = "Round {}: You could get {} points (the " \
                     "round {}'s data has been removed). The " \
                     "sum is: {}."
            round_points.append(2 * round_points[-1])
            print(report.format(iround+1, round_points[-1], iround, sum(round_points)))

        else:
            value = int(string)
            report = "Round {}: You could get {} points. The sum is: {}."
            round_points.append(value)
            print(report.format(iround+1, value, sum(round_points)))

        iround += 1

    return sum(round_points)


if __name__ == "__main__":
    # inp = ["5", "2", "C", "D", "+"]
    inp = ["5", "-2", "4", "C", "D", "9", "+", "+"]
    out = get_sum_of_points(inp)
