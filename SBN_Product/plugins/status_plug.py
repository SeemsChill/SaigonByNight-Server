# calculate the product status.
def status_calculator(current_quantity: int, product_quantity: int):
    # make sure its int.
    current_quantity = int(current_quantity)
    product_quantity = int(product_quantity)

    status_percentage = (current_quantity * 100) / product_quantity

    return int(status_percentage)

# check the status (red, yellow, green) via percentage.
def status_detector(status_percentage):
    # declare range.
    red_zone = 10       # from 10 -> 0.
    yellow_zone = 60    # from 60 -> 10.
    green_zone = 100    # from 100 -> 60.

    if status_percentage <= red_zone:
        return 'red'
    else:
        if status_percentage > yellow_zone:
            return 'green'
        else:
            return 'yellow'
