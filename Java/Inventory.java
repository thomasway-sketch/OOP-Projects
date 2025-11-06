package org.uob.a1;

public class Inventory {
    
    private String[] inventory;
    final private int inventorySize = 10;
    private int emptySlot;
    
    public Inventory(){
        this.emptySlot = 0;
        this.inventory = new String[this.emptySlot];
    }
    
    public String displayInventory(){
        String out = "";
        for(int i = 0; i<this.emptySlot; i++){
            out = out + this.inventory[i].split(" ", 2)[0] + " ";
            
        }
        return out;
    }
    
    public void addItem(String item){
        if(this.emptySlot < this.inventorySize){
            String[] newInventory = new String[this.emptySlot+1];
            for(int i =0; i<this.emptySlot; i++){
                newInventory[i] = this.inventory[i];
            }
            newInventory[this.emptySlot] = item;
            this.inventory = newInventory;
            this.emptySlot += 1;
        }
        else{
            System.out.println("Inventory full");
        }
    }
    
    public int hasItem(String item){
        int hasItem = -1;
        for(int i = 0; i<this.emptySlot;i++){
            if(item == this.inventory[i]){
                hasItem = 1;
            }
        }
        return hasItem;    
    }
    
    public void removeItem(String item){
        if(this.hasItem(item) == 1){
            String[] newInventory = new String[this.emptySlot-1];
            int k = 0;
            for(int i = 0; i < this.emptySlot; i++){
                if(this.inventory[i] != item){
                    newInventory[k] = this.inventory[i];
                    k++;
                    }
            }
            this.inventory = newInventory;
            this.emptySlot -= 1;
        }
        else{
            System.out.println("Item not in inventory");
        }

            
            /*
            int count = 0;
            boolean x = true;
            while(x){
                if(this.inventory[count] == item){
                    if(count == this.emptySlot-1){
                        this.inventory[count]=null;
                    }
                    else{
                        this.inventory[count] = null;
                        while(count < emptySlot){
                            count += 1;
                            this.inventory[count-1] = this.inventory[count];
                            this.inventory[count] = null;
                        }
                    }
                    x = false;
                }
                count++;
            }
        }*/
    }
    public int getEmptySlot(){
        return this.emptySlot;
    }
    public String[] getInventory(){
        return this.inventory;
    }
}