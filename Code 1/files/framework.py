import json
from enum import Enum
# import matplotlib
import matplotlib
import matplotlib.pyplot as plt
import matplotlib.cm as cm
from matplotlib import gridspec
import math

class Orientation(Enum):
    HORIZONTAL = 1  # rotated so wider than taller
    VERTICAL = 2  # rotated so taller than wider

class Box:
    def __init__(self, id, x, y):
        self.id = id
        self.area = x*y
        # Store dimensions in horizontal order
        if x > y:
            self.dims = (x, y)
        else:
            self.dims = (y, x)
        # Start off in horizontal state (you can change this attribute)
        self.orient = Orientation.HORIZONTAL

    def changed_orientated(self):
        """ Returns the dimensions of the box, orientated correctly for box """
        if self.orient == Orientation.HORIZONTAL:
            return self.dims
        else:
            return (self.dims[1], self.dims[0])

    def orientated(self):
        """ Returns the dimensions of the box, orientated correctly for box """
        if self.orient == Orientation.HORIZONTAL:
            return self.dims
        else:
            return (self.dims[1], self.dims[0])


class Container:
    def __init__(self, id, x, y):
        self.id = id
        self.dims = (x, y)
        self.area = x*y
        self.packed = []  # List of (Corner, Box) pairs
        self.corners = [Corner(0, 0)]  # Starting corner

    def pack(self, corner, box):
        """ Packs a box at a particular corner """
        self.packed.append((corner, box))

        # Remove used corner
        self.corners.remove(corner)
        # Add new top left corner
        self.corners.append(Corner(corner.pos[0],
                                   corner.pos[1] + box.changed_orientated()[1]))
        # Add new bottom left corner
        self.corners.append(Corner(corner.pos[0] + box.changed_orientated()[0],
                                   corner.pos[1]))

    def unpack_all(self):
        """ Unpack all boxes, returning them """
        removed_boxes = [b for (_c, b) in self.packed]
        self.packed = []
        self.corners = [Corner(0, 0)]
        return removed_boxes


class Corner:
    def __init__(self, x, y):
        self.pos = (x, y)

class Problem:
    """
    The problem instance and solution state mixed together

    Boxes should be moved from unpacked list into containers, and back to
    unpacked list again if container gets unpacked.
    """

    def __init__(self, filename):
        data = json.load(open(filename))
        self.start_logititude = data["start_pos"][0]["logititude"]
        self.start_latitude = data["start_pos"][0]["latitude"]

        self.conts = [Container(i, c["x"], c["y"])
                      for i, c in enumerate(data["containers"])]
        self.unpacked1 = [Box(i, c["x"], c["y"])
                         for i, c in enumerate(data["boxes"])]

        self.boxes = [Box(i, c["x"], c["y"])
                         for i, c in enumerate(data["boxes"])]
        self.cont = self.conts[0]
        self.unpacked = []
        id = 0
        for box in self.boxes:
            num_to_add = self.cont.area // box.area
            self.unpacked.extend([Box(id + i, box.dims[0], box.dims[1]) for i in range(num_to_add)])
            id += num_to_add
        print(len(self.unpacked1))

    def objective(self):
        tot = 0
        for cont in self.conts:
            for c, box in cont.packed:
                tot += box.area
        return tot

    def save_solution(self, file_name):
        boxes = []
        #for box in self.unpacked:
        #    boxes.append({"id": box.id})
        # TODO: reading this part carefully
        for cont in self.conts:
            for corn, box in cont.packed:
                boxes.append({
                    "id": box.id,
                    "logititude": self.start_logititude + corn.pos[0]/(1000*111*math.cos(self.start_logititude)),
                    "latitude": self.start_latitude + corn.pos[1]/(1000*111)})
        json.dump(boxes, open(file_name, "w"), indent=2)

    def plot(self, file_name=None):
        n_cols = 1000
        n_rows = 2
        n_conts = len(self.conts)
        fig = plt.figure(figsize=(8 * n_conts, 10))
        norm = matplotlib.colors.Normalize(vmin=0, vmax=20)
        cmap = cm.plasma
        m = cm.ScalarMappable(norm=norm, cmap=cmap)

        # Plot Containers
        g = gridspec.GridSpec(n_rows, n_cols, height_ratios=[3, 1])
        for cont in self.conts:
            col_start = int((cont.id * n_cols) / float(n_conts))
            col_end = int((cont.id + 0.9) * n_cols / float(n_conts))
            ax = fig.add_subplot(g[0, col_start:col_end])

            for corner, box in cont.packed:
                ax.add_patch(matplotlib.patches.Rectangle(
                    corner.pos,
                    box.changed_orientated()[0],
                    box.changed_orientated()[1],
                    edgecolor="black",
                    facecolor=m.to_rgba(box.area)))

                plt.text(corner.pos[0] + 0.5 * box.changed_orientated()[0],
                         corner.pos[1] + 0.5 * box.changed_orientated()[1],
                         str(box.id), ha="center")

            plt.xlim([0, cont.dims[0]])
            plt.ylim([0, cont.dims[1]])

        # Plot Unpacked Boxes
        ax = fig.add_subplot(g[1, 0:n_cols])
        ax.axis('off')
        x_pos = 0
        max_y = 1
        if len(self.unpacked) > 0:
            for box in self.unpacked:
                box_dims = box.changed_orientated()
                ax.add_patch(matplotlib.patches.Rectangle(
                    (x_pos, 0),
                    box_dims[0],
                    box_dims[1],
                    edgecolor="black",
                    facecolor=m.to_rgba(box.area)))

                plt.text(x_pos + 0.5 * box_dims[0], 0.5 * box_dims[1],
                         str(box.id), ha="center")

                x_pos += box_dims[0] + 1
                max_y = max(max_y, box_dims[1])

            plt.xlim([0, x_pos])
            plt.ylim([0, max_y * 2])

        if file_name is not None:
            fig.savefig(file_name)
        plt.show()
