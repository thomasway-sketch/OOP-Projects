package org.uob.a1;

import java.util.Scanner; // walls were a smart idea, puting the rooms in a two dimensional array also going to .lowercase the inputs. substrings, 2d array of features for looking around. used the split method for the item description

public class Game {  
    
    public static void main(String args[]) {
        // where ill write the main programme
        Scanner input = new Scanner(System.in);
        Inventory inventory = new Inventory();
        Score score = new Score(100);
        Map map = new Map(7,7);
        Room[][] rooms = new Room[7][7];
        Position posCheck = new Position(map.getPlayerPos().x,map.getPlayerPos().y);
        boolean directionValid = true;
        int looknum = -1;
        String[] useParts;
        boolean[] keys = {false, false, false};
        
        for(int y = 0; y<7;y++){
            for(int x = 0; x<7;x++){
                rooms[x][y] = new Room("Wall","A hard Stone wall stands infront of you. There does not seem a way to get past it.",'W', new Position(x,y));
            }
        }
        
        rooms[3][1] = new Room("The Entryway","Infront of you stands a massive door with three locks, one wooden lock, one combination lock and one keypad which seems to require a password.\nYou also see what looks to be a hallway behined you.", 'E', new Position(3,1));
        rooms[3][1].features = new String[4][2];
        rooms[3][1].featurenum = 4;
        rooms[3][1].features[0][0] = "wooden lock";
        rooms[3][1].features[1][0] = "combination lock";
        rooms[3][1].features[2][0] = "keypad";
        rooms[3][1].features[0][1] = "Inspecting the wooden lock you see a hole for a key";
        rooms[3][1].features[1][1] = "There are 4 digits on the combination lock";
        rooms[3][1].features[2][1] = "There is a keypad to type the password into";
        rooms[3][1].help = "You think you will need some more items to do anything in this room";
        rooms[3][1].flipEnterable();
            
        rooms[3][2] = new Room("A Fancy Hallway", "There are cold stone walls either side of you and a big chandelier overhead. Whoever built this place must be very rich.",'H',new Position(3,2)); // a monster will appear in this room the second time the  player enters it
        rooms[3][2].help = "There doesn't look like much to do hear";
        rooms[3][2].flipEnterable();
        
        rooms[3][3] = new Room("A Hallway","As you enter the stentch of gasoline hits you. There are cold stone walls either side of you and puddles which seem to be the source of the smell scattered all around the floor. There does not seem like anything to do hear but carry forward",'G', new Position(3,3));
        rooms[3][3].help = "gasoline may be useful if only you had something to pick it up";
        rooms[3][3].flipEnterable();
        rooms[3][3].features = new String[1][2];
        rooms[3][3].features[0][0] = "floor";
        rooms[3][3].features[0][1] = "There are puddles of gasoline on the floor";
        rooms[3][3].featurenum = 1;
        
        rooms[3][4] = new Room("A CrossRoads", "You enter a sqaure room and see three doors, each one on a different wall, and a tunnel which leads to the hallway you have already been through.\nLooking away from the hallway you see that the Wooden door on the right slightly creeking open and shut.\nThe Steel door in front of you looks to have the same combination lock as in the room with the huge door\nThe wooden door to the left does not seem to have a handle",'C', new Position(3,4));
        rooms[3][4].features = new String[3][2];
        rooms[3][4].featurenum = 3;
        rooms[3][4].features[0][0] = "wooden door";
        rooms[3][4].features[1][0] = "combination lock";
        rooms[3][4].features[0][1] = "pushing the door will not open it and there is no handle";
        rooms[3][4].features[1][1] = "There are 4 digits on the combination lock";;
        rooms[3][4].help = "There must be something you can use to open those doors around here";
        rooms[3][4].flipEnterable();

        rooms[2][4] = new Room("A Dining room", "In the center of the room there is a long rectangular dining table with 4 chairs on either side.\nThere are also two Wooden doors one leads to the fork in the road and another on the otherside of the room wide open leading to a dark room",'D', new Position(2,4)); // The player will be able to pick up the items on the table once
        rooms[2][4].features = new String[2][2];
        rooms[2][4].featurenum = 2;
        rooms[2][4].features[0][0] = "chair";
        rooms[2][4].features[1][0] = "dining table";
        rooms[2][4].features[0][1] = "Its a chair...";
        rooms[2][4].features[1][1] = "For each chair there is a empty plate, knife, fork and an empty glass.";
        rooms[2][4].help = "The table might have something useful on it";
        rooms[2][4].flipEnterable();
        
        rooms[1][4] = new Room("A dark room", "The room is too dark to see in except for a small radius around  the lamp in the middle of the room", 'L', new Position(1,4)); // there is a lamp in this room at the beggining until the player picks it up, the door will close
        rooms[1][4].features = new String[1][2];
        rooms[1][4].featurenum = 1;
        rooms[1][4].features[0][0] = "floor";
        rooms[1][4].features[0][1] = "Its a dimly lit lamp in the middle of the room";
        rooms[1][4].help = "That lamp will definitly be useful";
        rooms[1][4].flipEnterable();
        
        rooms[1][3] = new Room("The Vents", "Crawling through the vent is no easy feat, it is barely wide enough to fit your shoulders and for a second you panick thinking about getting stuck before calming yourself down", 'V', new Position(1,3));
        rooms[1][3].help = "Doesn't look like there is anything here";
        
        rooms[1][2] = new Room(" A Tiny room", "This room is barely wide enough to Stretch your arms out and as dark as the previous room. You think theyre might be something on the floor", 'T', new Position(1,2)); // there is a lighter. The player will have to use the lamp to see it
        rooms[1][2].features = new String[1][2];
        rooms[1][2].featurenum = 1;
        rooms[1][2].features[0][0] = "floor";
        rooms[1][2].features[0][1] = "its too dark to see whats on the ground";
        rooms[1][2].help = "Whats that on the ground";
        rooms[1][2].flipEnterable();

        rooms[4][4] = new Room("The Office", "You see a large desk at the back of the room covered in files and paperwork lit by a fancy chandelier. There is what seems to be a window behined the desk however it is borded up on the other side. There is a golden pen peaking out from under the paperwork", 'O', new Position(4,4)); // the pen will be a key and searching the desk will find the player the code for the steel door
        rooms[4][4].features = new String[2][2];
        rooms[4][4].featurenum = 2;
        rooms[4][4].features[0][0] = "window";
        rooms[4][4].features[1][0] = "desk";
        rooms[4][4].features[0][1] = "You try to smash through the window but it is sealed tight.";
        rooms[4][4].features[1][1] = "You look  through the drawers of the desk and find a small slip of paper with a code";
        rooms[4][4].help = "There must be something i can use in that desk";
        
        rooms[3][5] = new Room("The files", "You enter a massive room. All around you mountains of paperwork, you wonder how anyone would is able to find anything in this mess. At the end of the hallway you see a golden box", 'F', new Position(3,5)); // the golden key will open the box at the back of the room which contains the code that opens the huge door
        rooms[3][5].features = new String[1][2];
        rooms[3][5].featurenum = 1;
        rooms[3][5].features[0][0] = "golden box";
        rooms[3][5].features[0][1] = "Its a small box with a keyhole in the front";
        rooms[3][5].help = "How can you open that box";

        /*
        for(int y = 0; y<7; y++){
            for(int x = 0; x<7; x++){
                if(rooms[x][y].getSymbol() != 'w'){
                    map.placeRoom(rooms[x][y].getPosition(), rooms[x][y].getSymbol());
                }
            }
        }
        */
        
        System.out.println("Instructions:\nmove <direction> - (<direction> can be north, south, east, west). The player moves to a new room based on the direction.\nlook - Displays a description of the room.\nlook <feature> - Displays a more detailed description of a feature in a room.\nlook <item> - Displays a description of an item in the players inventory.\ngrab <item> - used to add items to your inventory\nuse move <item> <object> - uses an item on a specified object, items can be used on other items.\ninventory - Displays a list of all items the player has obtained.\nscore - Displays the players current score.\nmap - Displays a text-based map of the current explored game world.\nhelp - Displays a help message.\nquit - Quits the game");

        System.out.println("");

        System.out.println(rooms[map.getPlayerPos().x][map.getPlayerPos().y].getName());
        System.out.println("You wake up on a cold stone floor, water driping from a leak in the ceiling. You get up brimming with confidence wondering how you'll escape this time.\nAs you look around you realise that your not in another prison. After escaping every maximum security prison this world has to offer it seems they must have given up on keeping you contained in one. You see a compass, paper and a marker on the floor which you pick up. You think it will be useful to mark all the rooms you visit on the paper.");
        
        map.placeRoom(rooms[map.getPlayerPos().x][map.getPlayerPos().y].getPosition(),rooms[map.getPlayerPos().x][map.getPlayerPos().y].getSymbol());
        String command; 
        boolean gameActive = true;
        while(gameActive){
            command = input.nextLine();
            command = command.toLowerCase(); 
            if(command.length() > 5 && command.substring(0,4).equals("move")){
                score.visitRoom();
                if(command.substring(5).equals("north")){
                    posCheck.y -= 1;
                }
                else if(command.substring(5).equals("south")){
                    posCheck.y++ ;
                }
                else if(command.substring(5).equals("east")){
                    posCheck.x++;
                }
                else if(command.substring(5).equals("west")){
                    posCheck.x -= 1;
                }
                else{
                    System.out.println("Invalid direction");
                    directionValid = false;
                }
                if(directionValid){
                    map.placeRoom(rooms[posCheck.x][posCheck.y].getPosition(), rooms[posCheck.x][posCheck.y].getSymbol());
                }
                if(rooms[posCheck.x][posCheck.y].getEnterable()){
                    map.getPlayerPos().x = posCheck.x;
                    map.getPlayerPos().y = posCheck.y;
                    if(directionValid){
                        System.out.println("You enter " + rooms[posCheck.x][posCheck.y].getName());
                    }
                }
                else{
                    if(rooms[posCheck.x][posCheck.y].getSymbol() == 'W'){
                        System.out.println(rooms[posCheck.x][posCheck.y].getDescription());
                    }
                    else{
                        System.out.println("Cannot enter this room");
                        map.placeRoom(rooms[posCheck.x][posCheck.y].getPosition(), 'X');
                    }
                    posCheck.x = map.getPlayerPos().x;
                    posCheck.y = map.getPlayerPos().y;
                }
                directionValid = true;
            }

            else if(command.length() > 3 && command.substring(0,4).equals("look")){
                if(command.length() == 4 || command.length() == 5){
                    System.out.println(rooms[map.getPlayerPos().x][map.getPlayerPos().y].getDescription());
                }
                else{
                    for(int i = 0; i<rooms[map.getPlayerPos().x][map.getPlayerPos().y].featurenum; i++){
                        if(command.substring(5).equals(rooms[map.getPlayerPos().x][map.getPlayerPos().y].features[i][0])){
                            looknum = i;
                        }
                    }
                    if(looknum != -1){
                        System.out.println(rooms[map.getPlayerPos().x][map.getPlayerPos().y].features[looknum][1]);
                        looknum = -1;
                    }
                    else{
                        
                        for(int i = 0; i<inventory.getEmptySlot(); i++){
                            if(command.substring(5).equals(inventory.getInventory()[i].split(" ", 2)[0])){
                                looknum = i;
                            }
                        }
                        if(looknum != -1){
                            System.out.println(inventory.getInventory()[looknum].split(" ", 2)[1]);
                            looknum = -1;
                        }
                        else{
                            System.out.println("There is nothing of interest in the specified feature");
                        }
                    }
                }
            }

            else if(command.length() > 4 && command.substring(0,4).equals("grab")){
                if(rooms[map.getPlayerPos().x][map.getPlayerPos().y] == rooms[1][4] && command.substring(5).equals("lamp") && inventory.hasItem("lamp Can light up dark places") == -1){
                    inventory.addItem("lamp Can light up dark places");
                    rooms[1][4].features[0][1] = "A dimly lit lamp was in the middle of the room";
                    System.out.println("Item grabbed");
                }
                else if(rooms[map.getPlayerPos().x][map.getPlayerPos().y] == rooms[1][2] && command.substring(5).equals("lighter") && inventory.hasItem("lighter Could be used to burn something") == -1){
                    inventory.addItem("lighter Could be used to burn something");
                    rooms[1][2].features[0][1] = "There was a small lighter here";
                    System.out.println("Item grabbed");
                }
                else if(rooms[map.getPlayerPos().x][map.getPlayerPos().y] == rooms[2][4] && command.substring(5).equals("glass") && inventory.hasItem("glass Could be used to pick up liquids") == -1 ){
                    inventory.addItem("glass Could be used to pick up liquids");
                    rooms[2][4].features[1][1] = "For each chair there was a empty plate, knife, fork and an empty glass.";
                    rooms[3][3].setDescription("As you enter the stentch of gasoline hits you. There are cold stone walls either side of you and puddles which seem to be the source of the smell scattered all around you.");
                    System.out.println("Item grabbed");
                }

                else if(rooms[map.getPlayerPos().x][map.getPlayerPos().y] == rooms[4][4] && command.substring(5).equals("pen") && inventory.hasItem("pen A golden pen with reveals a key when clicked") == -1){
                    inventory.addItem("pen A golden pen with reveals a key when clicked");
                    rooms[4][4].setDescription("You see a large desk at the back of the room covered in files and paperwork lit by a fancy chandelier. There is what seems to be a window behined the desk however it is borded up on the other side.");
                    System.out.println("Item grabbed");
                }
                else if(rooms[map.getPlayerPos().x][map.getPlayerPos().y] == rooms[4][4] && command.substring(5).equals("code") && inventory.hasItem("code You think you should try this code on the combination lock") == -1){
                    inventory.addItem("code You think you should try this code on the combination lock");
                    rooms[4][4].features[1][1] = "There was a small slip of paper in the desk";
                    System.out.println("Item grabbed");
                }
                else{
                    System.out.println("You believe there is no use for the item specified or you have already picked it up");
                }
            }
            else if(command.length() > 3 && command.substring(0,3).equals("use")){
                useParts = command.split(" ", 3);
                if(useParts[1].equals("lamp") && inventory.hasItem("lamp Can light up dark places") == 1){
                    if(rooms[map.getPlayerPos().x][map.getPlayerPos().y] == rooms[1][2] && useParts[2].equals("floor")){
                        System.out.println("The lamp allows you to see a lighter on the floor");
                        score.solvePuzzle();
                    }
                    else if(rooms[map.getPlayerPos().x][map.getPlayerPos().y] == rooms[1][4] && useParts[2].equals("room") && !rooms[1][3].getEnterable()){
                        System.out.println("You see vents to the north");
                        rooms[1][3].flipEnterable();
                        score.solvePuzzle();
                    }
                }
                else if(useParts[1].equals("glass") && inventory.hasItem("glass Could be used to pick up liquids") == 1){
                    if(rooms[map.getPlayerPos().x][map.getPlayerPos().y] == rooms[3][3] && useParts[2].equals("floor")){
                        inventory.removeItem("glass Could be used to pick up liquids");
                        inventory.addItem("gasoline Could probably be lit on fire somehow");
                        System.out.println("Gasoline picked up");
                        score.solvePuzzle();
                    }
                }
                        
                else if(useParts[1].equals("lighter") && inventory.hasItem("lighter Could be used to burn something") == 1 && inventory.hasItem("gasoline Could probably be lit on fire somehow") == 1){
                    if(useParts[2].equals("gasoline")){
                        inventory.removeItem("lighter Could be used to burn something");
                        inventory.removeItem("gasoline Could probably be lit on fire somehow");
                        inventory.addItem("fire Enough flame to burn down a door");
                        System.out.println("You set the gasoline on fire");
                        score.solvePuzzle();
                    }
                }
                else if(useParts[1].equals("code") && inventory.hasItem("code You think you should try this code on the combination lock") == 1){
                    if(useParts[2].equals("combination lock")){
                        if(rooms[map.getPlayerPos().x][map.getPlayerPos().y] == rooms[3][4] && !rooms[3][5].getEnterable()){
                            System.out.println("Combination lock opened");
                            rooms[3][5].flipEnterable();
                            score.solvePuzzle();
                        }
                        else if(rooms[map.getPlayerPos().x][map.getPlayerPos().y] == rooms[3][1]){
                            System.out.println("Combination lock opened");
                            keys[0] = true;
                            score.solvePuzzle();
                        }
                    }
                }
                else if(useParts[1].equals("fire") && inventory.hasItem("fire Enough flame to burn down a door") == 1){
                    if(useParts[2].equals("wooden door") && rooms[map.getPlayerPos().x][map.getPlayerPos().y] == rooms[3][4] && !rooms[4][4].getEnterable()){
                        System.out.println("Door burnt down");
                        rooms[4][4].flipEnterable();
                        score.solvePuzzle();
                    }
                    if(useParts[2].equals("wooden lock") && rooms[map.getPlayerPos().x][map.getPlayerPos().y] == rooms[3][1]){
                        System.out.println("Lock burnt down");
                        keys[1] = true;
                        score.solvePuzzle();
                    }
                }
                else if(useParts[1].equals("pen") && inventory.hasItem("pen A golden pen with reveals a key when clicked") == 1 && rooms[map.getPlayerPos().x][map.getPlayerPos().y] == rooms[3][5] && useParts[2].equals("golden box")){
                    System.out.println("The box opened and inside was a password");
                    inventory.addItem("password Could be used on the keypad in the entryway");
                    score.solvePuzzle();
                }
                else if(useParts[1].equals("password") && rooms[map.getPlayerPos().x][map.getPlayerPos().y] == rooms[3][1] && useParts[2].equals("keypad") && inventory.hasItem("password Could be used on the keypad in the entryway") == 1){
                    System.out.println("Password accepted");
                    keys[2] = true;
                    score.solvePuzzle();
                }
                else{
                    System.out.println("The item is not in your inventory or it cannot be used here");
                }
            }
                
            else if(command.equals("inventory")){
                System.out.println(inventory.displayInventory());
            }
                
            
            else if(command.equals("score")){
                System.out.println(score.getScore());
            }
            
            else if(command.equals("map")){
                System.out.println(map.display());
            }
            
            else if(command.equals("help")){
                System.out.println(rooms[map.getPlayerPos().x][map.getPlayerPos().y].help);
            }
            
            else if(command.equals("quit")){
                System.out.println("Quiting game...");
                gameActive = false;
            }

            else{
                System.out.println("invalid command");
            }
            
            if(keys[0] && keys[1] && keys[2]){
                System.out.println("Suddenly the huge door infront of you opens up to show a green field. As you walk out you see a guy in a black suit walking up to you.\n You get ready to run but suddenly an electric shock run through your spine. As you slowly drift into unconsiousness you faintly hear the words - he's ready...");
                gameActive = false;
            }   
        }
    }
}        
