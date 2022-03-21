from framework import Orientation, Problem, Container, Corner, Box
import argparse
import os
import random as rand


def check_fit(cont: Container, corner: Corner, box: Box):
    """
    Check if box (with orientation set) fits at particular corner in container
    """
    assert (corner in cont.corners)

    # Find out the central point when putting the box on the given corner
    central_point_unpack_box = (
        corner.pos[0] + box.changed_orientated()[0] / 2, corner.pos[1] + box.changed_orientated()[1] / 2)

    # For each box that already in the container, check if the boxes are overlap
    for c, b in cont.packed:
        central_point = (c.pos[0] + b.changed_orientated()[0] / 2, c.pos[1] + b.changed_orientated()[1] / 2)
        horizontal_distance = abs(central_point_unpack_box[0] - central_point[0])
        vertical_distance = abs(central_point_unpack_box[1] - central_point[1])
        valid_min_horizontal_distance = (b.changed_orientated()[0] + box.changed_orientated()[0]) / 2
        valid_min_vertical_distance = (b.changed_orientated()[1] + box.changed_orientated()[1]) / 2
        if valid_min_horizontal_distance > horizontal_distance and valid_min_vertical_distance > vertical_distance:
            # Overlapping happens when the program goes in here
            return False

    # Check if the box outside the container and return True if the box still inside container
    return corner.pos[0] + box.changed_orientated()[0] <= cont.dims[0] \
           and corner.pos[1] + box.changed_orientated()[1] <= cont.dims[1]


def corner_heuristic(prob,
                     order_boxes=lambda x: x,
                     order_conts=lambda x: x,
                     order_corners=lambda x: x,
                     order_orients=lambda x: x
                     ):
    """ The corner heuristic algorithm """

    number_of_boxes = len(prob.unpacked)
    searched_boxes = set()

    # while len(searched_boxes) < number_of_boxes:
    for unpacked_box in order_boxes(prob.unpacked):
        print(unpacked_box.id)
        # print(len(searched_boxes))


        # Get the boxes and containers in order
        # in_order_boxes = order_boxes(prob.unpacked)
        in_order_containers = order_conts(prob.conts)

        # Selecting a box that has not been packed
        # for box in in_order_boxes:
        #     if box.id in searched_boxes:
        #         continue
        #     unpacked_box = box
        #     break

        # searched_boxes.add(unpacked_box.id)
        is_fit_in = False

        # For the selected box, check if it can fit in certain a corner in a certain container with certain orient
        # Once find one place to fit in, stop try other places
        for container in in_order_containers:
            corners_in_this_cont = order_corners(container.corners)
            for corner in corners_in_this_cont:
                for orient in order_orients(Orientation):
                    unpacked_box.orient = orient
                    if check_fit(container, corner, unpacked_box):
                        is_fit_in = True
                        container.pack(corner, unpacked_box)
                        # prob.unpacked.remove(unpacked_box)
                        break
                if is_fit_in:
                    break
            if is_fit_in:
                break


if __name__ == "__main__":
    par = argparse.ArgumentParser("2D Packing Corner Heuristic Solver")
    par.add_argument("file", help="json instance file")
    par.add_argument("--save-plot", default=None,
                     help="save plot to file")
    par.add_argument("--no-plot", action='store_true',
                     help="don't plot solution")

    args = par.parse_args()

    rand.seed(0)

    prob = Problem(args.file)
    # You can change the ordering functions here:
    corner_heuristic(prob,
                     # Boxes order
                     # Default
                     # order_boxes=lambda x: x,
                     # Reversed
                     # order_boxes=lambda x: reversed(x),
                     # Weight
                     order_boxes=lambda x: sorted(x, key=lambda x: x.area, reverse=True),
                     # Density
                     # order_boxes=lambda x: sorted(x, key=lambda x: x.density, reverse=True),

                     # Containers order
                     # Default
                     order_conts=lambda x: x,
                     # Reversed
                     # order_conts=lambda x: reversed(x),
                     # Remaining space
                     # order_conts=lambda x: x,

                     # Corners order
                     # Default
                     order_corners=lambda x: x,
                     # Reversed
                     # order_corners=lambda x: reversed(x),
                     # Random
                     # order_corners=lambda x: rand.sample(list(x), len(x)),

                     # Orients order
                     # Default
                     order_orients=lambda x: x
                     # Random
                     # order_orients=lambda x: rand.sample(list(x), 2)
                     )

    print(prob.objective())
    prob.save_solution(os.path.splitext(args.file)[0] + "-sol.json")
    if not args.no_plot:
        prob.plot(file_name=args.save_plot)
