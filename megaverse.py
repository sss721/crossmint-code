from enum import Enum
from typing import List
import requests
import time
import os
from dotenv import load_dotenv
load_dotenv()

class Shape(Enum):
    POLYANETS = "Polyanets"
    SOLOONS = "Soloons"
    COMETH = "Cometh"

class Megaverse:
    def __init__(self, row=11, col=11):
        self.ROW = row # Setting a default grid size for cross polyanets
        self.COL = col # Setting a default grid size for cross polyanets
        self.candidateId = os.getenv('candidateId') #2770084e-2d9c-4a1c-b8c9-1a16a1d67edc
        self.BASE_URL = "https://challenge.crossmint.io"
        self.POLYANETS_API  = "/api/polyanets"
        self.COMETHS_API = "/api/comeths"
        self.SOLOONS_API = "/api/soloons"
        self.GOAL_MAP_API = f"/api/map/{self.candidateId}/goal"
        self.headers = {'Content-type': "application/json"}


    def deleteShape(self, row: int, column: int, shape: Shape):
        """
        DELETE request to delete a shape at a given row and a column 
        @param: row: int
        @param: column: int
        @param: shape: Enum
        @return: None
        """

        if row < 0 or row >= self.ROW or column < 0 or column >= self.COL:
            print(f"Failed to Delete a {shape.value} at: row={row}, column={column}")
            return 
        
        points = { 
            "row": row,
            "column": column,
            "candidateId": self.candidateId 
        }

        shape_url = ''
        if shape == Shape.POLYANETS:
            shape_url = self.POLYANETS_API
        elif shape == Shape.COMETH:
            shape_url = self.COMETHS_API
        elif shape == Shape.SOLOONS:
            shape_url = self.SOLOONS_API

        try:
            cross_response = requests.delete(self.BASE_URL + shape_url, json=points, headers=self.headers)
            if cross_response.status_code == 200:
                print(f"Deleted {shape.value} at co-ordinates: row={row}, column={column}")
        except requests.exceptions.RequestException as err:
            print(f"Error while deleting {shape.value} ", err)

    def createPolyanets(self, row: int, column: int):
        """
        POST request to create a Polyanet
        @param: row: int
        @param: column: int
        @return: None
        """

        if row < 0 or row >= self.ROW or column < 0 or column >= self.COL:
            print(f"Failed to create a Polyanet at: row={row}, column={column}")
            return 
        
        points = { 
            "row": row,
            "column": column,
            "candidateId": self.candidateId 
        }

        time.sleep(3) # To avoid overloading the server
        try:
            cross_response = requests.post(self.BASE_URL + self.POLYANETS_API, json=points, headers=self.headers)
            if cross_response.status_code == 200:
                print(f"Created polyanet at co-ordinates: row={row}, column={column}")
        except requests.exceptions.RequestException as err:
            print("Error within polyanet post request ", err)

    def createCometh(self, row:int, column:int, direction: str):
        """
        POST request to create a Cometh
        @param: row: int
        @param: column: int
        @param: direction: str
        @return: None
        """

        if row < 0 or row >= self.ROW or column < 0 or column >= self.COL:
            print(f"Failed to create a Cometh at: row={row}, column={column}")
            return 
        
        points = { 
            "row": row,
            "column": column,
            "direction": direction,
            "candidateId": self.candidateId 
        }
        time.sleep(5) # To avoid overloading the server
        try:
            cross_response = requests.post(self.BASE_URL + self.COMETHS_API, json=points, headers=self.headers)
            if cross_response.status_code == 200:
                print(f"Created cometh at co-ordinates: row={row}, column={column}")
        except requests.exceptions.RequestException as err:
            print("Error within cometh post request ", err)
    

    def createSoloons(self, row: int, column: int, color: str):
        """
        Post request to create a Soloon

        @param: row: int
        @param: column: int
        @param: color: str
        @return: None
        """

        if row < 0 or row >= self.ROW or column < 0 or column >= self.COL:
            print(f"Failed to create a Soloon at: row={row}, column={column}")
            return 
        
        points = { 
            "row": row,
            "column": column,
            "color": color,
            "candidateId": self.candidateId 
        }
        time.sleep(3) # To avoid overloading the server
        try:
            cross_response = requests.post(self.BASE_URL + self.SOLOONS_API, json=points, headers=self.headers)
            if cross_response.status_code == 200:
                print(f"Created soloon at co-ordinates: row={row}, column={column}")
        except requests.exceptions.RequestException as err:
            print("Error within soloon post request ", err)


    def getGoalMap(self) -> List[List] | None:
        """
        Get the goal map of polyanets, soloons and comeths

        @param: None
        @return: List[]
        """

        try:
            goal_map_response = requests.get(self.BASE_URL + self.GOAL_MAP_API)
            if goal_map_response.status_code == 200:
                return goal_map_response.json()['goal']
        except requests.exceptions.RequestException as err:
            print("Error", err)


    def createPolyanetsCross(self):
        """
        Creating the cross using polyanets. Since the cross grid's initial setup starts 
        after 2 rows and ends 2 rows before the minimum row length expected is 5.
        @params: None
        @return: None
        """
        if self.ROW != self.COL or self.ROW < 5:
            print(f"Failed to create a cross polyanets pattern. Check row and column sizes!")
            return 
        
        end_row_col = self.ROW - 3
        start_row_col = 2

        for i in range(start_row_col, end_row_col+1):
            self.createPolyanets(i, i)
            j = start_row_col + end_row_col - i
            if i != j:
                self.createPolyanets(i, j)

    def createCrossmintLogo(self):
        """
        Creating the crossmint logo with soloons and comeths

        @param: None
        @return: None
        """

        goalGrid = self.getGoalMap()
        if goalGrid:
            self.ROW = len(goalGrid)
            self.COL = len(goalGrid[0])
            

            for r in range(self.ROW):
                for c in range(self.COL):
                    gridValue = goalGrid[r][c].lower()

                    if gridValue != "space":
                        if gridValue == "polyanet":
                            self.createPolyanets(r, c)
                        else:
                            values = gridValue.split('_')

                            if values[1] == "soloon":
                                self.createSoloons(r, c, values[0])
                            elif values[1] == "cometh":
                                self.createCometh(r, c, values[0])
        else:
            print("Can't create the megaverse as Goal map is empty")
