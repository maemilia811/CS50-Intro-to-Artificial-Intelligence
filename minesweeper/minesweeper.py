import itertools
import random


class Minesweeper():
    """
    Minesweeper game representation
    """

    def __init__(self, height=8, width=8, mines=8):

        # Set initial width, height, and number of mines
        self.height = height
        self.width = width
        self.mines = set()

        # Initialize an empty field with no mines
        self.board = []
        for i in range(self.height):
            row = []
            for j in range(self.width):
                row.append(False)
            self.board.append(row)

        # Add mines randomly
        while len(self.mines) != mines:
            i = random.randrange(height)
            j = random.randrange(width)
            if not self.board[i][j]:
                self.mines.add((i, j))
                self.board[i][j] = True

        # At first, player has found no mines
        self.mines_found = set()

    def print(self):
        """
        Prints a text-based representation
        of where mines are located.
        """
        for i in range(self.height):
            print("--" * self.width + "-")
            for j in range(self.width):
                if self.board[i][j]:
                    print("|X", end="")
                else:
                    print("| ", end="")
            print("|")
        print("--" * self.width + "-")

    def is_mine(self, cell):
        i, j = cell
        return self.board[i][j]

    def nearby_mines(self, cell):
        """
        Returns the number of mines that are
        within one row and column of a given cell,
        not including the cell itself.
        """

        # Keep count of nearby mines
        count = 0

        # Loop over all cells within one row and column
        for i in range(cell[0] - 1, cell[0] + 2):
            for j in range(cell[1] - 1, cell[1] + 2):

                # Ignore the cell itself
                if (i, j) == cell:
                    continue

                # Update count if cell in bounds and is mine
                if 0 <= i < self.height and 0 <= j < self.width:
                    if self.board[i][j]:
                        count += 1

        return count

    def won(self):
        """
        Checks if all mines have been flagged.
        """
        return self.mines_found == self.mines


class Sentence():
    """
    Logical statement about a Minesweeper game
    A sentence consists of a set of board cells,
    and a count of the number of those cells which are mines.
    """

    def __init__(self, cells, count):
        self.cells = set(cells)
        self.count = count

    def __eq__(self, other):
        return self.cells == other.cells and self.count == other.count

    def __str__(self):
        return f"{self.cells} = {self.count}"

    def known_mines(self):
        """
        Returns the set of all cells in self.cells known to be mines.
        """
        if(len(self.cells) == self.count): 
            return self.cells
        return None

    def known_safes(self):
        """
        Returns the set of all cells in self.cells known to be safe.
        """
        if(len(self.cells) == 0): 
            return self.cells
        return None

    def mark_mine(self, cell):
        """
        Updates internal knowledge representation given the fact that
        a cell is known to be a mine.
        """
        if (cell in self.cells):
            self.cells.remove(cell)
            self.count -= 1

    def mark_safe(self, cell):
        """
        Updates internal knowledge representation given the fact that
        a cell is known to be safe.
        """
        if (cell in self.cells):
            self.cells.remove(cell)


class MinesweeperAI():
    """
    Minesweeper game player
    """

    def __init__(self, height=8, width=8):

        # Set initial height and width
        self.height = height
        self.width = width

        # Keep track of which cells have been clicked on
        self.moves_made = set()

        # Keep track of cells known to be safe or mines
        self.mines = set()
        self.safes = set()

        # List of sentences about the game known to be true
        self.knowledge = []

    def mark_mine(self, cell):
        """
        Marks a cell as a mine, and updates all knowledge
        to mark that cell as a mine as well.
        """
        self.mines.add(cell)
        for sentence in self.knowledge:
            sentence.mark_mine(cell) 

    def mark_safe(self, cell):
        """
        Marks a cell as safe, and updates all knowledge
        to mark that cell as safe as well.
        """
        self.safes.add(cell)
        for sentence in self.knowledge:
            sentence.mark_safe(cell) #Corregir aca 

    def add_knowledge(self, cell, count): 
        """
        Called when the Minesweeper board tells us, for a given
        safe cell, how many neighboring cells have mines in them.

        This function should:
            1) mark the cell as a move that has been made
            2) mark the cell as safe
            3) add a new sentence to the AI's knowledge base
               based on the value of `cell` and `count`
            4) mark any additional cells as safe or as mines
               if it can be concluded based on the AI's knowledge base
            5) add any new sentences to the AI's knowledge base
               if they can be inferred from existing knowledge
        """

        #mark the cell as a move that has been made
        self.moves_made.add(cell)

        #mark the cell as safe
        self.mark_safe(cell)

        #create a list with neighbours of the cell
        neighbours = []

        if (cell[0] == 0 and cell[1] == 0): 
            neighbours.extend([(0,1), (1,0), (1,1)])
        elif(cell[0] == 0 and cell[1] == self.width - 1):
            neighbours.extend([(0,6),(1,6),(1,7)]) 
        elif(cell[0] == self.height - 1 and cell[1] == 0):
            neighbours.extend([(6,0),(6,1),(7,1)])
        elif(cell[0] == self.height - 1 and cell[1] == self.width - 1):
            neighbours.extend([(6,6),(6,7),(7,6)])
        elif(cell[0] >= 1 and cell[0] <= self.height - 2 and cell[1] == 0):
            neighbours.extend([(cell[0]-1,0),(cell[0]-1,1),
                                             (cell[0],1),
                               (cell[0]+1,0),(cell[0]+1,1)])
        elif(cell[0] >= 1 and cell[0] <= self.height - 2 and cell[1] == self.width - 1):
            neighbours.extend([(cell[0]-1,6),(cell[0]-1,7),
                               (cell[0],6),
                               (cell[0]+1,6),(cell[0]+1,7)])
        elif(cell[0] == 0 and cell[1] >= 1 and cell[1] <= self.width - 2):
            neighbours.extend([(0,cell[1]-1),            (0,cell[1]+1),
                               (1,cell[1]-1),(1,cell[1]),(1,cell[1]+1)])
        elif(cell[0] == self.height - 1 and cell[1] >= 1 and cell[1] <= self.width - 2):
            neighbours.extend([(6,cell[1]-1),(6,cell[1]),(6,cell[1]+1),
                               (7,cell[1]-1),            (7,cell[1]+1)])
        else:
            neighbours.extend([(cell[0]-1,cell[1]-1),(cell[0]-1,cell[1]),(cell[0]-1,cell[1]+1), 
                               (cell[0], cell[1]-1),                     (cell[0],cell[1]+1),
                               (cell[0]+1,cell[1]-1),(cell[0]+1,cell[1]),(cell[0]+1,cell[1]+1)])
            

        #add a new sentence to the AI's knowledge base
        sentence = Sentence(neighbours,count)

        #Be sure to only include cells whose state is still undetermined in the sentence.
        for c in sentence.cells:
            if (cell in self.mines):
                self.mark_mine(c)
            elif(cell in self.safes):
                self.mark_safe(c)

        #add the sentence to the knowledge
        self.knowledge.append(sentence)
        
        #Check subsets. 
        sets = []
        for s in self.knowledge: 
            new = Sentence(s.cells - sentence.cells, s.count - sentence.count)
            sets.append(new)
        
        self.knowledge.extend(sets)

        #If, based on any of the sentences in self.knowledge, new cells can be marked as safe or as mines, then the function should do so.
        mines = []
        safes = []
        for sentence in self.knowledge: 
            if (sentence.known_mines() != None):
                mines.extend(sentence.known_mines())
            if (sentence.known_safes() != None):
                safes.extend(sentence.known_safes())
        
        if (mines != []):
            for m in mines:
                self.mark_mine(m)
        if (safes != []):
            for s in safes:
                self.mark_safe(s)   


    def make_safe_move(self):
        """
        Returns a safe cell to choose on the Minesweeper board.
        The move must be known to be safe, and not already a move
        that has been made.

        This function may use the knowledge in self.mines, self.safes
        and self.moves_made, but should not modify any of those values.
        """
 
        for i in range(self.height):
            for j in range(self.width): 
                cell = (i,j)
                if(cell not in self.moves_made and 
                   cell in self.safes): 
                    return (i,j)
        
        return None 



    def make_random_move(self): 
        """
        Returns a move to make on the Minesweeper board.
        Should choose randomly among cells that:
            1) have not already been chosen, and
            2) are not known to be mines
        """
        cells = {(i, j) for i in range(self.height) for j in range(self.width)}
        
        cells -= self.moves_made
        cells -= self.mines 

        cells_list = list(cells)

        move = random.choice(cells_list)
        
        return move



#All changes required in Sentence are done- 
#make_safe_move and make_random_move is done 