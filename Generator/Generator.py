import numpy as np
import matplotlib.pyplot as plt
from matplotlib.patches import Circle, Rectangle
from shapely import geometry
import math

class Generator:
    def __init__(self, image_width=500, image_height=500, seed=None):
        self.num_images = 0
        self.image_width = image_width
        self.image_height = image_height
        self.seed = seed

        self.circle_ratio = []
        self.square_ratio = []
        self.circle_square_ratio = []

        self.min_square_side_length = 24
        self.min_circle_radius = 12
        self.max_circle_radius = image_width / 4
        self.max_square_side_length = image_width / 2

        if seed == None:
            rand_seed = np.random.randint(0, 1000)
            np.random.seed(rand_seed)
            self.seed = rand_seed
            print(f"Seed not provided. Using random seed {rand_seed}")
        else:
            print(f"Seed provided. Using seed {seed}")
            np.random.seed(seed)

    def generate_images(self, draw_random=False, draw_circle=False, draw_square=False, directory="dataset", quantity=1):
        # np.random.seed(self.seed)
        i = 0

        while i < quantity:
            if draw_random:
                draw_circle = np.random.choice([True, False])
                draw_square = np.random.choice([True, False])
            background_color = self._generate_nonmatching_color()
            
            fig = plt.figure(figsize=(self.image_width/100, self.image_height/100), facecolor=background_color, linewidth=0.0)
            ax = fig.add_subplot(111)
            ax.set_rasterized(True)
            
            if draw_square:
                filename = "square_"
                square_color = self._generate_nonmatching_color(background_color)
                side_length = np.random.uniform(self.min_square_side_length, self.max_square_side_length)
                square_x = np.random.uniform(0, self.image_width - side_length)
                square_y = np.random.uniform(0, self.image_height - side_length)   
                square_angle = np.random.uniform(0, 360)                   
              
                center_x = square_x + side_length / 2
                center_y = square_y + side_length / 2
                square = Rectangle((square_x, square_y), side_length, side_length, color=square_color, angle=square_angle, rotation_point=(center_x, center_y))
                square.set_antialiased(True)
                corners = square.get_corners()
                shape_square = geometry.Polygon(corners)

                # Check if square is outside image bounds
                if self._cornerOutOfBounds(corners[0][0], corners[0][1]) or \
                    self._cornerOutOfBounds(corners[1][0], corners[1][1]) or \
                    self._cornerOutOfBounds(corners[2][0], corners[2][1]) or \
                    self._cornerOutOfBounds(corners[3][0], corners[3][1]):
                    plt.close()
                    continue

               
                ax.add_patch(square)
                # change ratio based on size
                self.square_ratio.append(side_length / self.image_width)
            if draw_circle:
                if draw_square:
                    filename += "circle_"
                else:
                    filename = "circle_"
                circle_color = self._generate_nonmatching_color(background_color)
                radius = np.random.uniform(self.min_circle_radius, self.max_circle_radius)
                circle_x = np.random.uniform(0, self.image_width - radius)
                circle_y = np.random.uniform(0, self.image_height - radius)

                if draw_square:
                    # check with shapely if circle intersects square
                    shape_circle = geometry.Point(circle_x, circle_y).buffer(radius)
                    if shape_square.intersects(shape_circle):
                        plt.close()
                        continue
       

                # Check if circle is outside image bounds
                if circle_x - radius < 0 or circle_x + radius > self.image_width or \
                    circle_y - radius < 0 or circle_y + radius > self.image_height:
                    plt.close()
                    continue
                
                if draw_square:
                    self.circle_square_ratio.append((radius * 2) / side_length)

                circle = Circle((circle_x, circle_y), radius, color=circle_color)
                circle.set_antialiased(True)
                ax.add_patch(circle)
                # change ratio based on size
                self.circle_ratio.append(radius * 2 / self.image_width)

            ax.set_xlim(0, self.image_width)
            ax.set_ylim(0, self.image_height)
            ax.set_aspect('equal', adjustable='box')
            ax.axis('off')
            if draw_square == False and draw_circle == False:
                filename = "none_"
            plt.tight_layout()
            plt.savefig(f'{directory + "/" + filename + str(i+1)}.png', bbox_inches='tight', pad_inches=0, dpi=106.5)
            plt.close()
            self.num_images += 1
            i += 1

    def _generate_nonmatching_color(self, *excluded_colors):
        while True:
            color = np.random.rand(3)
            if all(np.linalg.norm(color - excluded) > 0.1 for excluded in excluded_colors):
                return color
    
    

    def _cornerOutOfBounds(self, x, y):
        if x < 0:
            return True
        if x > self.image_width:
            return True
        
        if y < 0:
            return True
        if y > self.image_height:
            return True

        return False
    
    def getAverageRatio(self):
        return (np.mean(self.circle_ratio).round(2),
                 np.mean(self.square_ratio).round(2),
                   np.mean(self.circle_square_ratio).round(2))

        