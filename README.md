# **Langton's Ant Simulation**

**Project Name:** Langton's Ant Enhanced  

# Description
This project implements **Langton's Ant**, a classic cellular automaton that demonstrates simple rule-based behavior leading to complex emergent patterns. This version expands upon the traditional simulation by introducing **customizable ant behaviors, and dynamic tile transformations.**

# **Features**

✅ **Core Langton's Ant Rules** → The ant follows standard movement rules based on tile states.  
✅ **Extended Tile Types** → Various Tile type each influencing ant movement uniquely.  
✅ **Extended Ant Types** → There also variety of Ant type that exhibit different behavior when faced with tile's movement rule.  
✅ **Grid-Based World Management** → A structured **World** class handles tile updates and interactions.  
✅ **Modular Components** → Simply create a new ant type or tile type by creating a class inheriting the base Ant/Tile.  

# **Technical Details**

- **Core Components:**
    - `Tile` → Define the tile that influence ant's movements
    - `World` → Simulates interactions between tiles and ants
    - `Ant` → Defines different ant behaviors

# **Potential Enhancements**

- [x] **Multi-State Tiles** → Tiles could cycle through additional states before flipping.  
- [x] **Customizable Ant Logic** → Add ants with unique movement patterns beyond standard behavior.  
- [ ] **Interactive Initialization** → Implement grid editor to define the initial state of simulation.
- [ ] **Import / Export** → Implement a way to save the state of grid so it can be export and import.
