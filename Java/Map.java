package org.uob.a1;

public class Map {

    private char[][] map;
    private int xSize;
    private int ySize;
    final private char EMPTY = '.';
    private Position playerPos;
    
    public Map(int xSize, int ySize){
        this.playerPos = new Position(3,1);
        this.xSize = xSize;
        this.ySize = ySize;
        this.map = new char[this.ySize][this.xSize];
        for(int y = 0; y<this.ySize; y++){
            for(int x=0; x<this.xSize; x++){
                this.map[y][x] = EMPTY;
            
            }
        }
    }
            
    /*
    public String locationDisplay(){
        char[][] tempMap = this.map;
        tempMap[this.playerPos.x][this.playerPos.y] = '@';
        String map ="";
        for(int y =0; y<this.ySize; y++){
            for(int x=0; x<this.xSize; x++){
                map = map + tempMap[x][y];
            }
            map = map + "\n";
        }
        
        return map;
    }
    */

    public String display(){
        String map ="";
        for(int y =0; y<this.ySize; y++){
            for(int x=0; x<this.xSize; x++){
                map = map + this.map[x][y];
            }
            map = map + "\n";
        }
        
        return map;
    }
            
    public void placeRoom(Position pos, char symbol){
        this.map[pos.x][pos.y] = symbol;
    }
    public Position getPlayerPos(){
        return this.playerPos;
        }
}