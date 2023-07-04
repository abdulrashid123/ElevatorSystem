# `Elevator System`
    This Django project implements an elevator system that can handle elevator operations,
    such as moving up and down, opening and closing doors, starting and stopping running,
    and displaying the current status. The system also assigns the most optimal elevator to 
    user requests based on a list of requests.

##`Design Decisions`

    The project is built using Django and Django REST Framework (DRF) to provide a robust and scalable solution for the elevator system.
    The elevator system is represented by the Elevator model, which stores information about each elevator's availability, operational status, current floor, and destination floor.
    Floor requests are represented by the Request model, which stores the requested floor, direction (up or down), and the associated elevator.
    The project utilizes DRF's ModelViewSet to handle CRUD operations for the Elevator and UserRequest models.
    The system assigns floor requests to elevators based on a FIFO logic that can be implemented in the assign_elevator function it also handles concurrency problems
    The API endpoints follow RESTful conventions and provide clear and concise responses.Postgres is used as DB for better and realtime performance


##`API Contracts`

    The API contracts for the elevator system are as follows:

1. ###`System Api`:
       - POST /system/: Create a new System
         required fields:[name]
         
         ex:{"name":"Sample System"}

2. ### `Elevator Api`
        - POST /elevator/: Create 'n' elevators 
          
            required fields:[system,floors]
          
            ex:{"system":1,"floors":5}
          
        - GET /elevator/?system=1&status=MOVING UP  get elevators with given status in system
        
            required params:[system,status]
        
        - GET /elevator/1/?next=direction get elevator next destination
        
            required params:[next]
        
        - GET /elevator/1/ get elevator of given id it also includes requests received by elevator
        
            required params:[next]
        
        - UPDATE /elevator/1/ update elevator transitions
            
            required fields:[floor,status]
          
            ex:{"status":"IDLE","floor":4}
    
        **NOTE** for status choices are ['IDLE','MOVING UP','MOVING DOWN','DOOR OPEN','DOOR CLOSED','STOPPED']
    

3. ### `Request Api`
    
        - POST /request/: Create Request to get access to elevator 
        
            required fields:[system,floor]
          
            ex:{"system":1,"floor":4}
      
        

##`Setup, Deploy, and Test`
    
    To set up, deploy, and test the elevator system, follow these steps:

    1. Clone the repository: git clone <repository-url>
    2. Change to the project directory: cd elevator_system_project
    3. Install the project dependencies: pip install -r requirements.txt
    4. Set up the database by running migrations: python manage.py migrate
    5. (Optional) Configure any necessary settings in settings.py, such as the database connection or caching.
    
    Start the development server: python manage.py runserver
    Access the API endpoints using a tool like cURL, Postman, or any HTTP client.

##`Additional Notes`
    If using PostgreSQL as the database, ensure that the necessary configurations are added to
    settings.py and the PostgreSQL database is set up and accessible.
    
    While using update method of elevator api sould be called in sequential manner ex : when
    DOOR OPEN is called DOOR CLOSED should be called next instead of any other choices








