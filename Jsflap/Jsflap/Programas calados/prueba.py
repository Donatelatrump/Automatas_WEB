from Pytomatas.dfa import DFA

# Creates a DFA called "my_dfa":
my_dfa = DFA()

# Define to "my_dfa" a set of states names:
my_dfa.setStates( {"q0", "q1", "qfinal"} )

# Define to "my_dfa" a set of states characters of the alphabet:
my_dfa.setAlphabet( {"a", "b"} )

# Set the "Initial state" name of "my_dfa":
my_dfa.setInitial( "q0" )

# Define to "my_dfa" the set of "Final states" names:
my_dfa.setFinals( {"qfinal", "qf2"} )

# Add transitions to the DFA:
my_dfa.addTransition( ("q0", "a", "q1") )
my_dfa.addTransition( ("q0", "b", "qfinal") )
my_dfa.addTransition( ("q1", "a", "q1") )
my_dfa.addTransition( ("q1", "b", "q1") )
my_dfa.addTransition( ("qfinal", "a", "qfinal") )
my_dfa.addTransition( ("qfinal", "b", "qfinal") )

# Add more data to the existing one already in the automata:
my_dfa.addSymbol("c")
my_dfa.addState("qx")
my_dfa.addState("finalState2")
my_dfa.addFinal("finalState2")

# Prints the DFA information:
my_dfa.show()

# Check if a string is accepted on the defined automata "my_dfa":
# It returns True or False if the string is accepted or not:
word = "aaabb"
my_dfa.accepts(word)

# Checks if the string is accepted, but prints all the process and steps on transitions;
# Shows the flow of states while reading the string;
my_dfa.accepts(word, stepByStep=True)