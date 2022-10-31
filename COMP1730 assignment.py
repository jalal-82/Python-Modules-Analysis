# -*- coding: utf-8 -*-
"""
Created on Tue Oct  4 13:06:19 2022

@author: DELL_XPS15
"""
import sys
import platform 
import importlib


def pversion():
    return sys.version_info

from isort.stdlibs.py39 import stdlib
# Import all package name inside the standard library  

def get_stdlibs_packages():
    '''

    Returns the python version using sys
    and all internal package name excluding those starting with '_'
    -------
    stdList : List

    '''
    #Note: I am not using sys.version here as i used another method in function 
    # below called pversion().
    
    listyList = sorted(stdlib)
    # Local Variable of Package in List and Alphabetical Order
    
    stdList = [name for name in listyList if (name[0]) != '_']
    # Packages that doesn't Start with '_'
    # Note: my package does't contain this and antigravity so I didn't do 
    # anything regardign those.
    
    return stdList

def task1():
    '''
    Returns
    Python and OS version followed by first 5 and last 5 module in get_stdlibs_packages()

    '''
    
    print('StdLib contains ' + str(len(get_stdlibs_packages()))+
          " modules where First 5 and last 5 modules on Python " + platform.python_version()+ 
          " on " + platform.system() +" "+ platform.version())
    
    stdList = get_stdlibs_packages()
    
    for i in range(0,5):
        print(stdList[i])
        # Print First 5 Modules
        
    for i in range(len(stdList)-5,len(stdList)):
        print(stdList[i])
        # Print Last 5 Modules
        
def get_real():
    '''
    Returns
    All modules which are importable on this python version
    TYPE: List which contains module type
    '''
    validList = []
    # create empty set
    
    i = 0
    
    listyList = sorted(stdlib)
    # Convert stdlib from set to sorted list
    
    while i<len(listyList):
        
        name = listyList[i]
        
        if (name[0] != '_'):
            # Avoid all modules that begin with '_'
            
            try:
                module = importlib.import_module(name)
                # Check If module is importable
                
                validList.append(module)
                # Add the module to the List
            except:
                # If not importable then skip and move on
                pass
        i = i+1
    return validList
        
def fail_real():
    '''
    Returns
    All modules which are not importable on this python version
    TYPE: List which contains module type
    '''
    i = 0
    NonValidList = []
    
    listyList = sorted(stdlib)
    # Convert stdlib from set to sorted list

    
    while i<len(listyList):
        name = listyList[i]
        try:
            module = importlib.import_module((name))
            # If importable then skip and move on
            pass
        
        except:
            NonValidList.append(module)
            # If not importable then add to NonValidList
        i = i+1
    return NonValidList

def os_pversion():
    return "These StdLib modules on Python " + platform.python_version() + " / " + platform.system() + " " + platform.version() + " are not importable "

def task2():
    '''
    Returns
    Modules which aren't imporable in this python version
    Type = str + List(module)

    '''
    print("These StdLib modules on Python " + platform.python_version() +
          " / " + platform.system() + " " + platform.version() + 
          " are not importable " )
    
    print(str(fail_real()))
        
def module_dependency(module_names, name): 
    '''

    Parameters
    ----------
    module_names : List 
        List of modules from task 2
    name : str
        a module name in string format
    Returns
    The exact modules which input name is dependent on from input module_name 
    
    dependentModules : List
        List of modules
    '''
    
    moduleList = module_names
    #convert functions into local variable to increase speed of output
    
    for currentModule in moduleList:

        if (vars(currentModule)['__name__'] == name):
            # check if name of currentmodule is same as the input name
            givenModule = currentModule
        
    dependentModules = [module for module in vars(givenModule).values() if (module) in moduleList]
    # Use List comprehension to check for module from vars if that module is in input module list
    
    return dependentModules

def len_module_dependency(givenModule): 
    '''
    Parameters
    givenModule : Module
    
    Returns
    This function returns the number of dependecies in a module
    TYPE : Integer
        
    '''
    
    moduleList = get_real()
    
    dependentModules = [module for module in vars(givenModule).values() if (module) in moduleList]
    #Similar as module_dependency(module_names, name) Line 156 
    
    return len(dependentModules)


def CoreDependent():
    '''
    Returns
    All Modules in get_real() which has no dependecies 
    Type = list
    
    '''
    
    core_module = [vars(module)['__name__'] for module in get_real() if (len(module_dependency(get_real(), vars(module)['__name__']))==0)]
    #Check if the number of module dependent of each module from importable module is 0
    
    return core_module

      
def five_Most_dependent(): 
    '''
    Returns 5 most dependent modules and the exact number of dependencies 
    Type = Tuple inside a list where first element is string of module name and
    second element is integer representing number of modules it is dependent on. 
    '''
    
    moduleList = get_real()    
    
    orderedByDependencies = sorted(moduleList, key = len_module_dependency, reverse=True)
    # Sort ModuleList from ascending to descending by it's number of dependencies
    
    Length_Module_By_dependency = [(vars(module)['__name__'],len_module_dependency(module)) for module in orderedByDependencies if (len(module_dependency(get_real(), vars(module)['__name__'])))]
    # Create tuple which represent module name in string and int of dependency length 

    return Length_Module_By_dependency[:5]
    # Return first 5 values of Length_Module_By_dependency

            
def task3():
    '''
    Returns 5 most dependent modules and the exact number of dependencies 
    And All core modules including it's length and module names. 
    Type = Tuple inside a list where first element is string of module name and
    second element is integer representing number of modules it is dependent on. 
    
    COre module length is an integer and the module names are string.
    
    '''

    fivemostdependent = five_Most_dependent()
    #Increase speed of function
    
    print("The following StdLib packages are most dependent:")
    
    for name in fivemostdependent:
        print(name) 
    
    coreModules = CoreDependent()
    #Increase speed of function
    
    print('The ' +str(len(coreModules))+ ' core modules are ')
    
    for name in coreModules:
        print(name, end=' '+', ')
        # Print list of module name Horizontally

def python_only_modules():
    '''
    Returns modules files which end with .py (python coded file)
    Type = List
    '''

    moduleList = get_real()
    
    outputList = []
    
    for module in moduleList:
        if '__file__' in vars(module):
            # Find all __file__ atributes to avoid built-in modules
            outputList.append(module)
            # if file directory is in vars then add to outputList
            
    return outputList

def explore_package(a_package):
    '''

    Parameters
    ----------
    a_package : MODULE
        Insert a python coded module  
    Returns
    (Number of Lines of coding, Number of classes)
    
    Note: Class only 

    '''
    
    filePath = a_package.__file__   
    # Directory of module
    
    currentFile = open(filePath, 'r', encoding='utf-8',errors='ignore')
    # open the file of module 
    #endoding and error is used to avoid unknown unicode error on some specfic modules
    
    classes = [line for line in currentFile if (line.startswith("class "))]
    # go through all line and find ones that starts with 'classes ' 
    
    currentFile.seek(0)
    # when finished with classes, go all the to top of file 
    
    lines = sum(1 for line in currentFile)
    #Now count all lines of coding including empty lines
                                                
    currentFile.close()
    #close the file
    
    return(lines, len(classes))


def task4():
    '''
    Returns
    
    5 largest files interms of number of coding
    5 Smallest files interms of number of coding
    5 largest files interms of number of classes
    Name of packages with no custom classes
    -------
    Type: Str + tuple + list 
    '''
    
    moduleList = python_only_modules()
    
    classesList = [[explore_package(module),module.__name__] for module in moduleList]
    
    sorted_classList = sorted(classesList, key= lambda f:f[0][1], reverse = True)
    # Sort from ascending to descending in terms of number of classes in the module
    
    sorted_linesList = sorted(classesList, key= lambda f:f[0][0], reverse = True)
    # Sort from ascending to descending in terms of number of lines of coding in the module

    print("These are the 5 largest packages in terms of the number of lOC")
    
    for i in sorted_linesList[0:5]:
        #Print largerst 5 in terms in line of coding
        print(i)
        
    print("These are the 5 Smallest packages in terms of the number of lOC")
    
    for i in sorted_linesList[-5:]:
        # print 5 Smallest files in terms of number of coding
        print(i)
        
    print("These are the 5 largest packages in terms of the number of Classes")

    for i in sorted_classList[0:5]:
        # print largest 5 in terms of number of classes defined
        print(i)
    
    print("These are the packages with 0 number of Classes")
    
    i=0
    
    while i < len(sorted_classList):
        
        numClasses = sorted_classList[i][0][1]
        # local variable of number of classes
        if numClasses == 0:
            
            print(sorted_classList[i][1])
            # print the name of module 
            i=i+1
        else:
            pass 
        i =i+1
        
def task5(permutation):
    '''
    

    Parameters
    ----------
    permutation : Set

    Returns
    Closed sets of the permutation
    sets : List
        This function doesn't work exactly as asked by task5.
        However, it can take in a set and will tell if two elements
        are mapped to same value also called permutation.
        it can take set like 
        {'hello' : 'hi', 'bye' : 'bye', 'hi' : 'morning','night' : 'night', 'morning' : 'hello'}
        and return [['hello', 'hi', 'morning'], ['bye'], ['night']]
        I struggled to undertsand the exact problem of task5. 

    '''
    sets = []
    checked =[]
    #Create empty lists
    
    for i in permutation:
        mod = i
        
        val = permutation[mod]
        
        SET = []
        
        if mod not in checked:
            SET.append(mod)
            # if module is not in checked list then add it to SET list
            
        while val not in SET and val != mod and val not in checked:
            SET.append(val)
            mod=val
            if mod not in checked:
                checked.append(mod)
            if mod in permutation:
                val = permutation[mod]
        if i not in checked:
            checked.append(i)
        if SET !=[]:
            sets.append(SET)
    return sets

def analyse_stdlib():
    # task1()
    # task2()
    # task3()
    # task4()
    return task1(),task2(),task3(),task4()
    
if __name__ == '__main__':
    NAME = 'Jalal Khan'
    ID   = 'u7480662'
    print(f'My name is {NAME}, my id is {ID}, and these are my findings for Project COMP1730.2022.S2')
    analyse_stdlib()