/****************************************************************************************************
* CS461-Artificial Intelligence - Fall 2018
* Homework#2
* Group : Puzzle_Busters
* Submission Date : 05/11/2018
****************************************************************************************************/

/****************************************** Description *********************************************
* Program to print path from root node to destination node for 9-puzzle after the solving process.
* Algorithm using " Branch and Bound search ".
*
* The 9-puzzle is a game in which there are nine 1x1 tiles arranged on a form composed of a 1x1 square
* and a 3x3 square (cf. image below) so that there is one 1x1 uncovered (empty) area on the form.
* The tiles are labeled 1 through 9, and initially they are shuffled. The idea is to reach the goal
* state (cf. image below) from a given initial state by moving tiles one at a time.
*
* You can find more details in the report file in.pdf format.
* Thank You 🙂
****************************************************************************************************/
#include <bits/stdc++.h>
#include <conio.h>
using namespace std;
/* N is the dimention of the sub-puzzle */
#define N 3

/* initPuzzle is the initial value of the 9-puzzle generated by GeneratePuzzle function*/
std::vector<int> initPuzzle;

/* goalPuzzle is the value of the 9-puzzle that we want to reach */
std::vector<int> goalPuzzle;

/* blank tile coordinates */
int blankX,blankY;

/* state space tree nodes */
struct Node
{
    /* stores parent node of current node, it helps in tracing path when answer is found */
    Node* parent;

    /* stores matrix */
    int mat[N][N];

    /* stores blank tile coordinates */
    int x, y;

    /* stores the number of misplaced tiles */
    int cost;

    /* stores the number of moves so far */
    int level;
};

/*====================================== IsSolvable ===============================================
* Description : Find if the generated 9-puzzle is solvable or Unsolvable.
* Input       : 9-puzzle as a vector<int>
* Output      : Boolean value ( True ~ Solvable | False ~Unsolvable )
=================================================================================================*/
bool IsSolvable(vector<int> puzzle)
{
    int inversion = 0;
    for (int i=0; i<puzzle.size(); i++)
    {
        for (int j=i+1; j<puzzle.size(); j++)
        {
            if (puzzle[j]!=0 && puzzle[i]!=0 && puzzle[i]>puzzle[j])
            {
                inversion++;
            }
        }
    }
    return (inversion%2==0);
}

/*=================================== GeneratePuzzle ==============================================
* Description : Generate the initial, shuffled and solvable, 9-puzzle.
* Input       : Unshuffled 9-puzzle as a vector<int>
* Output      : shuffled 9-puzzle as a vector<int>
=================================================================================================*/
vector<int> GeneratePuzzle(vector<int> puzzle)
{
    bool solvable=false;
    random_shuffle(puzzle.begin(),puzzle.begin()+2);
    int shuffleBegin = 2;
    if(puzzle[0]==1)shuffleBegin=1;
    while(!solvable)
    {
        random_shuffle(puzzle.begin()+shuffleBegin,puzzle.end());
        if(IsSolvable(puzzle))
        {
            solvable=true;
        }
    }
    return puzzle;
}

/*=================================== ShowPuzzle ==================================================
* Description : Print the 9-puzzle.
* Input       : 9-puzzle as a vector<int>
* Output      : No output
=================================================================================================*/
void ShowPuzzle(vector<int> puzzle)
{
    cout<<" _"<<endl<<"|";
    for (int i=0; i<puzzle.size(); i++)
    {
        if(i==1)cout<<"___"<<endl<<"|";
        if(i==4 || i==7)cout<<endl<<"|";
        cout<<puzzle[i]<<"|";
    }
    cout<<endl;
}

/*=================================== GetBlank ====================================================
* Description : Search for the blank tile in the 9-puzzle.
* Input       : 9-puzzle as a vector<int> ; x and y as pointers to the blank tile coordinates.
* Output      : No output
=================================================================================================*/
void GetBlank(vector<int> puzzle, int &x,int &y)
{
    int i = 0;
    while (i < puzzle.size())
    {
        if (puzzle[i]!=0)
            i++;
    }
    if (i==0){x=0;y=0;}
    else if (i<0){x=1;y=i-1;}
    else if (i<6){x=2;y=i-4;}
    else {x=3;y=i-7;}
}

/*=================================== GetBlankXY =================================================
* Description : Search for the blank tile in the 8-puzzle.
* Input       : 8-puzzle as a vector<int> ; x and y as pointers to the blank tile coordinates.
* Output      : No output
=================================================================================================*/
int GetBlankXY(int initial[N][N], int & x,int &y)
{

    int j,i = 0;
    int blankCoord=0;
    while (i < 3 && blankCoord==0)
    {
        j=0;
        while(j<3 && blankCoord==0)
        {
            if (initial[i][j]==0)
            {
                x=i;
                y=j;
                blankCoord=1;
            }
            j++;
        }
        i++;
    }
    return 0;
}

/*=================================== NextMove ====================================================
* Description : Print the next move in order to solve the 9-puzzle.
* Input       : coord. of blank tile in initial_state and final_state of the 9-puzzle as a vector<int>
* Output      : No output
=================================================================================================*/
void NextMove(int X, int Y, int puzzle[N][N])
{
    int x,y;
    GetBlankXY(puzzle,x,y);
    if (X!=x || Y!=y)
    {
        cout<<"------"<<endl;
        if(X<x) cout<<"  UP";
        if(X>x) cout<<" DOWN";
        if(Y<y) cout<<" LEFT";
        if(Y>y) cout<<" RIGHT";
        cout<<endl<<"------"<<endl;
        blankX = x;
        blankY = y;
    }
}

/*=================================== ShowPath ====================================================
* Description : Print different states of the 9-puzzle during the solving process.
* Input       : initial_state and final_state of the 9-puzzle as a vector<int>
* Output      : No output
=================================================================================================*/
void ShowPath(int mat[N][N])
{
    cout<<" _"<<endl<<"|1|___"<<endl;
    for (int i = 0; i < N; i++)
    {
        cout<<"|";
        for (int j = 0; j < N; j++)
            printf("%d|", mat[i][j]);
        cout<<endl;
    }
}

/*=================================== Puzzle8To9 ==================================================
* Description : Create a 9-puzzle from an 8-puzzle to print the path.
* Input       : an 8-puzzle as a Matrix NxN
* Output      : a 9-puzzle as vector<int>
=================================================================================================*/
vector<int> Puzzle8To9(int puzzle8[N][N])
{
    vector<int> puzzle9;
    puzzle9[0]=1;
    for(int i=0; i<3; i++)
        for(int j=0; j<3; j++)
            puzzle9[3*i+j+1] = puzzle8[i][j];
    return puzzle9;
}

/*===================================== newNode ==================================================
* Description :  Allocate a new node. (!) we find this code in " www.geeksforgeeks.org "
* Input       : tree as matrix NxN; blank tile coord.; current level; prent node.
* Output      : a new node.
=================================================================================================*/
Node* newNode(int mat[N][N], int x, int y, int newX,int newY, int level, Node* parent)
{
    Node* node = new Node;

    /* set pointer for path to root */
    node->parent = parent;

    /* copy data from parent node to current node */
    memcpy(node->mat, mat, sizeof node->mat);

    /* move tile by 1 postion */
    swap(node->mat[x][y], node->mat[newX][newY]);

    /* set number of misplaced tiles */
    node->cost = INT_MAX;

    /* set number of moves so far */
    node->level = level;

    /* update new blank tile coordinates */
    node->x = newX;
    node->y = newY;

    return node;
}

/* bottom, left, top, right */
int row[] = { 1, 0, -1, 0 };
int col[] = { 0, -1, 0, 1 };

/*=================================== CalculateCost ===============================================
* Description :  calculate the the number of misplaced tiles
*                ie. number of non-blank tiles not in their goal position.
* Input       :  two matrix NxN.
* Output      :  calculated cost as int.
=================================================================================================*/
int CalculateCost(int initial[N][N], int final[N][N])
{
    int cost = 0;
    for (int i = 0; i < N; i++)
        for (int j = 0; j < N; j++)
            if (initial[i][j] && initial[i][j] != final[i][j])
                cost++;
    return cost;
}

/*====================================== IsSafe ===================================================
* Description :  Check if (x, y) is a valid matrix coordinates.
* Input       :  pointers to tile coordinates.
* Output      :  positive int if it's true and negative integer if it's not.
=================================================================================================*/
int IsSafe(int x, int y)
{
    return (x >= 0 && x < N && y >= 0 && y < N);
}

/*====================================== PrintPath ================================================
* Description :  Print path from root node to destination node.
* Input       :  root node.
* Output      :  No output
=================================================================================================*/
void PrintPath(Node* root)
{
    if (root == NULL)
        return;
    PrintPath(root->parent);
    NextMove(blankX,blankY,root->mat);
    ShowPath(root->mat);
}

/* Comparison object to be used to order the heap (!) we find this code in " www.geeksforgeeks.org " */
struct comp
{
    bool operator()(const Node* lhs, const Node* rhs) const
    {
        return (lhs->cost + lhs->level) > (rhs->cost + rhs->level);
    }
};

/*======================================= BranchAndBound ==========================================
* Description : Solve the sub-puzzle (8-puzzle)using the Branch and Bound.
* Input       : an 8-puzzle as a Matrix NxN ; pointers to the blank tile coord. in initial state.
* Output      : No output
=================================================================================================*/
void BranchAndBound(int initial[N][N], int x, int y, int final[N][N])
{
    /* Create a priority queue to store live nodes of search tree */
    priority_queue<Node*, vector<Node*>, comp> pq;

    /* create a root node */
    Node* root = newNode(initial, x, y, x, y, 0, NULL);

    /* calculate the Node cost */
    root->cost = CalculateCost(initial, final);

    /* Add root to list of live nodes */
    pq.push(root);

    /* Finds a live node with least cost,
    add its childrens to list of live nodes
    and finally deletes it from the list */
    while (!pq.empty())
    {
        /* Find a live node with least estimated cost */
        Node* min = pq.top();

        /* The found node is deleted from the list of live nodes */
        pq.pop();

        /* print the path from root to destination if min is an answer node */
        if (min->cost == 0)
        {
            PrintPath(min);
            return;
        }

        /* do for each child of min max 4 children for a node */
        for (int i = 0; i < 4; i++)
        {
            if (IsSafe(min->x + row[i], min->y + col[i]))
            {
                /* create a child node */
                Node* child = newNode(min->mat, min->x,
                                      min->y, min->x + row[i],
                                      min->y + col[i],
                                      min->level + 1, min);

                /* Calculate the child node cost */
                child->cost = CalculateCost(child->mat, final);

                /* Add child to list of live nodes */
                pq.push(child);
            }
        }
    }
}

/*************************************************************************************************
***************************************** Main ***************************************************
*************************************************************************************************/
int main()
{


    /* gives the random_shuffel function a new seed */
    srand ( unsigned (time(0)));

    /* Goal configuration where value 0 is used for empty space*/
    for(int i=0; i<10; i++)
        goalPuzzle.push_back(i);

    /* Goal configuration used in solve to solve the sub-puzzle */
    int final[N][N] =
    {
        {0, 2, 3},
        {4, 5, 6},
        {7, 8, 9}
    };

    /* Call of GeneratePuzzle for the initial configuration */
    initPuzzle=GeneratePuzzle(goalPuzzle);

    /* Create a sub-puzzle of the 9-puzzle which is an 8-puzzle */
    /* initial configuration of the sub-puzzle */
    int initial[N][N];
    for(int i=0; i<3; i++)
        for(int j=0; j<3; j++)
            initial[i][j]=initPuzzle[3*i+j+1];

    /* Print the initial configuration */
    cout<<"Generated Puzzle"<<endl;
    ShowPuzzle(initPuzzle);

    /* Start solving the 9-puzzle */
    /* start with the case where blank tile is in the 1x1 square */
    cout<<endl<<"9-puzzle solving path"<<endl;
    ShowPuzzle(initPuzzle);
    if(initial[0][0]==1)
    {
        initial[0][0]=0;
        initPuzzle[0]=1;
        initPuzzle[1]=0;
        cout<<"------"<<endl<<"  UP"<<endl<<"------"<<endl;
        /* Print the next configuration if the blank tile was in the 1x1 square */
        //ShowPuzzle(initPuzzle);
    }

    int x,y;
    /* Blank tile coordinates in initial configuration */
    GetBlankXY(initial, x, y);
    blankX = x;
    blankY = y;

    /* Call of the Solving function of the sub-puzzle (8-puzzle) */
    BranchAndBound(initial, x, y,final);


    /* Print the last state */
    cout<<"------"<<endl<<" DOWN"<<endl<<"------"<<endl;
    ShowPuzzle(goalPuzzle);

    /* Holding the console open after running the program */
    getch();

    return 0;
}

