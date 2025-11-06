package org.uob.a1;

public class Room {

    private String name;
    private String description;
    private char symbol;
    private Map map;
    private Position position;
    public String help;
    public String[][] features;
    public int featurenum;
    private boolean enterable; 
    
    public Room(String name, String description, char symbol, Position position){
        this.name = name;
        this.description = description;
        this.symbol = symbol;
        this.position = position;
        this.features = new String[0][0];
        this.featurenum =0;
        this.enterable = false;
    }
    public String getName(){
        return this.name;
    }
    public String getDescription(){
        return this.description;
    }
    public char getSymbol(){
        return this.symbol;
    }
    public Position getPosition(){
        return this.position;
    }
    public void flipEnterable(){
        this.enterable = !this.enterable;
    }
    public boolean getEnterable(){
        return this.enterable;
    }
    public void setDescription(String descrip){
        this.description = descrip;
    }
        
}


    