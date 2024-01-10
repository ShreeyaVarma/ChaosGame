import math
import random
import matplotlib.pyplot as plt
from matplotlib.patches import Path
from matplotlib.transforms import Affine2D

# plt.figure(figsize=(6, 5))


class Chaos:

    def __init__(self, n, vertices, number_of_points, fraction_of_dist):
        """
        Constructor of the Class
        :param vertices: represents the corners of the polygon
        :param number_of_points: represents the dots to be drawn inside the polygon
        :param fraction_of_dist: represents the fraction of distance between the previous point and the next point
        """
        self.number_of_sides = n
        self.vertices_name = {chr(ord('A') + i): i for i in range(n)}
        self.polygon = Path(vertices)
        self.points = number_of_points
        self.r = fraction_of_dist
        self.previous_index = None  # for maintaining points' records later

    def show_polygon(self):
        """
        Plots the polygon as a patch on 2D plane
        :return: the shape of the polygon
        """
        if self.number_of_sides == 3:
            plt.plot(*zip(*self.polygon.vertices))  # zips and separates into x and y
        else:
            # rotates the figure by certain angle and saves it as original
            rotation = Affine2D().rotate_deg(-45)
            rotated_polygon = self.polygon.transformed(rotation)
            self.polygon = rotated_polygon
            plt.plot(*zip(*self.polygon.vertices))

    def random_coor(self):
        """
        Generates a point's coordinates randomly and plots if it's contained in the polygon area
        :return: the calculated point
        """
        while True:
            x = random.uniform(0, 1)
            y = random.uniform(0, 1)
            if self.polygon.contains_point((x, y)):
                return x, y

    def random_vertex(self):
        """
        Calculates the random vertex to be chosen for the next iteration
        :return: the index of the calculated vertex
        """
        max_vertex_index = len(self.polygon.vertices) - 2
        # '-2' as indices for lists start from 0 upto len-1 and 1st index repeats thus to prevent repeated count

        if max_vertex_index == 2:
            vertex_index = random.randint(0, max_vertex_index)
        else:
            # special condition for n>3
            vertex_index = random.randint(0, max_vertex_index)
            while (vertex_index == self.previous_index) and (not (self.previous_index is None)):
                vertex_index = random.randint(0, max_vertex_index)

        self.previous_index = vertex_index
        return vertex_index

    def move_towards_vertex(self, starting_point, which_vertex):
        """
        Calculates the total amount of distance to travel from starting to the destination point and sets it as position of the new vertex
        :param starting_point: at which the point initially plotted
        :param which_vertex: the destination vertex after travelling the fraction distance
        :return: the vertex to move towards after each iteration
        """

        vertex_choice = self.polygon.vertices[which_vertex]

        dx, dy = vertex_choice[0] - starting_point[0], vertex_choice[1] - starting_point[1]
        new_x, new_y = starting_point[0] + dx * self.r, starting_point[1] + dy * self.r
        return new_x, new_y

    def label_vertices(self):
        """
        Labels the vertices of the polygon
        :return: returns the labelled vertices in the plot
        """
        x_coors, y_coors = zip(*self.polygon.vertices)
        max_x = max(x_coors)
        max_y = max(y_coors)

        labels = [vert for vert in self.vertices_name]

        for index, (x, y) in enumerate(self.polygon.vertices[:-1]):
            ha = 'left'  # shown as right
            va = 'bottom'  # shown as top

            if x < max_x / 2:
                ha = 'right'  # shown as left
            if y < max_y / 2:
                va = 'top'  # as top
            plt.text(x, y, labels[index], ha=ha, va=va)

    def plotting(self):
        """
        Displays the final output of the game by plotting the grid
        :return: the polygon with the points according to the iterations and the fraction of distance
        """
        self.show_polygon()
        self.label_vertices()
        font = {'family': 'serif', 'color': 'blue', 'size': 15}
        plt.title('CHAOS', fontdict=font)

        points_list = [self.random_coor()]

        for i in range(self.points - 1):
            # properly displays polygon with all sides
            points_list.append(self.move_towards_vertex(points_list[-1], self.random_vertex()))
        plt.scatter(*zip(*points_list), s=0.1, c='k')  # joins 2 lists into the elements of a single list
        plt.show()


def polygon_radius(sides):
    """
    Mathematically calculates the radius of the polygon inorder to make it a unit side length polygon
    :param sides: takes the total number of sides of the polygon
    :return: the radius of polygon
    """
    theta = (2 * math.pi) / sides  # center angle
    alpha = (math.pi - theta) / 2  # equal angle of isosceles triangle
    radius = math.sin(alpha) / math.sin(theta)  # distance between centre to vertex of polygon
    return radius


def polygon_vertices(sides, radius):
    """
    Creates the coordinates of the vertices from the input of number of sides
    :param sides: total number of sides of the polygon
    :param radius: distance from center of polygon to the vertex
    :return: the vertices of the polygon
    """
    one_segment = math.pi * 2 / sides

    points = [
        (round(math.sin(one_segment * i) * radius, 4),
         round(math.cos(one_segment * i) * radius, 4))
        for i in range(sides)]

    return points


# for dna

def read_file_data(file):
    """
    Reads and cleans/collects the entire data in the file
    :param file: represents the location where the file exists
    :return: the data inside the file
    """
    file = open("HumanY_data.txt", 'r')
    data = file.read()
    clean_data = data.replace('\n', '')
    file.close()
    return clean_data


def unique_char(data):
    """
    Calculates the total unique characters present in the file and groups them into a dictionary
    :param data: the text file with all the DNA bases as characters
    :return: the unique characters in the data file
    """
    d = {}
    index = 0
    for vert in data:
        if not (vert in d):
            d[vert] = index
            index += 1
    return d


class GeneticSequence(Chaos):

    def __init__(self, file_path, r, rad, sides_num):
        """
        Constructor of the DNA class
        :param file_path: represents the location of the text file with all the data
        :param r: represents the fraction of distance
        """
        self.file_data = read_file_data(file_path)
        self.r = r
        self.radius_square = rad
        self.number_of_sides = sides_num
        self.vertices_name = unique_char(self.file_data)

        vertices = polygon_vertices(len(self.vertices_name), radius=2)
        vertices += [vertices[0]]  # last point's coordinates repeats to make a complete polygon.

        self.polygon = Path(vertices)
        self.show_polygon()
        self.label_vertices()

    def plotting(self):
        """
        Executes the entire diagram and forms the grid
        :return: plot of the structure with the points sequence
        """
        font = {'family': 'serif', 'color': 'blue', 'size': 15}
        plt.title('Genetic Sequence', fontdict=font)

        points_list = [self.random_coor()]

        for vertex in self.file_data:
            index = self.vertices_name[vertex]
            points_list.append(self.move_towards_vertex(points_list[-1], index))
        plt.scatter(*zip(*points_list), s=0.00001, c='k')  # alpha=0.5, cmap='nipy_spectral')
        plt.show()


def choice_1_chaos(n, number_of_points, fraction_of_dist):
    """
    Helps execute the chaos game representation
    :param n: represents the number of sides of the polygon
    :param number_of_points: total number of dots to be plotted
    :param fraction_of_dist: distance between consecutive points
    :return: the final structure plot
    """
    rad = polygon_radius(n)
    p = polygon_vertices(n, rad)
    vertices = p + [p[0]]  # structure as [(0, 0), (1, 0), (1, 1), (0, 1), (0, 0)]
    print("Calculating random points and plotting according to form the chaos...\n")
    c = Chaos(n, vertices, number_of_points, fraction_of_dist)
    c.plotting()


def choice_2_dna(fraction_of_dist):
    """
    Helps execute the genetic sequence of DNA bases
    :param fraction_of_dist: the ratio of distance between previous and next point in plot
    :return: the plot of chromosome distribution of human genome
    """
    rad = polygon_radius(4)
    sides_num = 4
    print("Calculating the points and plotting according to the DNA bases...\n")
    d = GeneticSequence("HumanY_data.txt", fraction_of_dist, rad, sides_num)
    d.plotting()


def main():
    """
    Takes input from the user about the details of the figure (menu-driven)
    :return: plots the chromosome distribution of the human genome using the chaos game logic
    """
    while True:
        print("1: Chaos Game")
        print("2: Genetic Sequence")
        print("3: Quit\n")

        ch = int(input("Enter the choice of your display: "))

        if ch == 1:
            n = int(input("Enter number of sides that the polygon should have: "))  # 3
            number_of_points = int(input("Enter number of iterations: "))
            fraction_of_dist = float(input("Enter the fraction of distance: "))
            choice_1_chaos(n, number_of_points, fraction_of_dist)

        elif ch == 2:
            fraction_of_dist = float(input("Enter the fraction of distance: "))
            choice_2_dna(fraction_of_dist)

        elif ch == 3:
            break

        else:
            print("Please enter a valid input choice from the above. ")


main()
