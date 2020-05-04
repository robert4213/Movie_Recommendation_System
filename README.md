# Movie_Recommendation_System

## Database ERD   
![Database ERD](https://github.com/robert4213/Movie_Recommendation_System/blob/master/SQL_ERD.jpg)



## API  
### Search   
get a list of searched movies   
get localhost/movieSearch?search=${search}   
Return:   
[   
    {   
        id:123,   
        title:'HP4',   
        poster:'https://images-na.ssl-images-amazon.com/images/I/517A4QTR22L._SY445_.jpg'   
    },   
    {   
        id:125,   
        title:'HP5',   
        poster:'https://images-na.ssl-images-amazon.com/images/I/517A4QTR22L._SY445_.jpg'   
    }   
]  

### Recommendation
get a list of recommended movies   
get localhost/movieSuggestion?userId=${userId}   
Return:   
[   
    {   
        id:123,   
        title:'HP4',   
        poster:'https://images-na.ssl-images-amazon.com/images/I/517A4QTR22L._SY445_.jpg'   
    },   
    {   
        id:125,   
        title:'HP5',   
        poster:'https://images-na.ssl-images-amazon.com/images/I/517A4QTR22L._SY445_.jpg'   
    }   
]  


### Rating Record
get a list of rated movies   
get localhost/moviesRating?userId=${userId}   
Return:   
[   
    {   
        id:123,   
        title:'HP4',   
        poster:'https://images-na.ssl-images-amazon.com/images/I/517A4QTR22L._SY445_.jpg'   
        rating:3   
    },   
    {   
        id:125,   
        title:'HP5',   
        poster:'https://images-na.ssl-images-amazon.com/images/I/517A4QTR22L._SY445_.jpg'   
        rating:4    
    }   
]  

### Update Rating Record
post a new movie rating   
post localhost/movieRating   
Update:   
{   
    movieId: 123,   
    userId: test1,   
    rating:5   
}   
Return:   
Nothing in body   


### Movie Detail
post a movie detail information and user's rating   
get localhost/movie?movieId=123&userId='test1'  
Return:  
{   
    id:123,   
    title:'HP4',   
    genre:'Fantasy',   
    poster:'https://images-na.ssl-images-amazon.com/images/I/517A4QTR22L._SY445_.jpg',   
    director:'Unknown',   
    actor:'Emma Watson',   
    avg_rating:4,   
    released:'2012',   
    description:'Harry Potter 4',    
    user_rating:4    
}   
