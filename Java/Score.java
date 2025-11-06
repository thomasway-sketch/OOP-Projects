package org.uob.a1;

public class Score {

    private int startingScore;
    private final int PUZZLE_VALUE = 10;
    private int roomsVisited;
    private int puzzlesSolved;
    
    public Score(int startingScore){
        this.startingScore = startingScore;
    }
    public int getScore(){
        return this.startingScore + (PUZZLE_VALUE * puzzlesSolved) - (roomsVisited);
    }
    public void visitRoom(){
        this.roomsVisited++;
    }
    public void solvePuzzle(){
        this.puzzlesSolved++;
    }
    
}