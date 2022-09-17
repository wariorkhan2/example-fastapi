from fastapi import FastAPI,Response,status,HTTPException,Depends,APIRouter
from sqlalchemy.orm import Session
from .. import models,schemas,utils,oauth2
from typing import List,Optional
from ..database import get_db
from sqlalchemy import func

router = APIRouter(
    prefix= "/posts",
    tags=["posts"]
)




################################
@router.get("/",response_model=List[schemas.PostOut])
async def get_posts(db: Session = Depends(get_db),current_user:int =Depends (oauth2.get_current_user),limit:int = 10,skip:int=0,search:Optional[str]=""):

    # cursor.execute("""select * from posts""")
    # post = cursor.fetchall()
    #return{"data":post}
    #posts = db.query(models.Post).filter(models.Post.title.contains(search)).limit(limit).offset(skip).all()
    
    posts = db.query(models.Post,func.count(models.Vote.post_id).label("votes")).join(models.Vote,models.Vote.post_id==models.Post.id,isouter=True).group_by(models.Post.id).filter(models.Post.title.contains(search)).limit(limit).offset(skip).all()
    #results = db.query(models.PostOut,func.count(models.Vote.post_id).label("votes")).join(models.Vote,models.Vote.post_id==models.PostOut.id,isouter=True).group_by(models.PostOut.id).filter(models.PostOut.title.contains(search)).limit(limit).offset(skip).all()
    
    return posts
################################



##################################
@router.post("/",status_code = status.HTTP_201_CREATED,response_model = schemas.Post)
async def create_post(post: schemas.PostCreate,db: Session = Depends(get_db),current_user: int = Depends(oauth2.get_current_user)):
    # cursor.execute("""insert into posts(title,content,published) values(%s,%s,%s) returning *""",(post.title,post.content,post.published))
    # new_post = cursor.fetchall()
    # conn.commit()

    new_post = models.Post(owner_id=current_user.id, **post.dict())
    db.add(new_post)
    db.commit()
    db.refresh(new_post)
    return new_post	


############################################

#,response_model=schemas.PostOut

##########################################
@router.get("/{id}",response_model=schemas.PostOut)
async def get_post(id: int, response:Response,db: Session = Depends(get_db),current_user:int = Depends(oauth2.get_current_user)):
    # cursor.execute("""select * from posts where id=%s """,(str(id)))
    # post = cursor.fetchone()
    # print(post)

    #post = db.query(models.Post).filter(models.Post.id == id).first()
    post = db.query(models.Post,func.count(models.Vote.post_id).label("votes")).join(models.Vote,models.Vote.post_id==models.Post.id,isouter=True).group_by(models.Post.id).filter(models.Post.id == id).first()
    if not post:
        raise HTTPException(status_code = status.HTTP_404_NOT_FOUND,
                            detail = f"post with id {id} not found"
                            )
    return post
#############################################



#############################################
@router.delete("/{id}",status_code = status.HTTP_204_NO_CONTENT)
def delete_post(id:int,db: Session = Depends(get_db),current_user :int = Depends(oauth2.get_current_user)):
    # cursor.execute("""delete from posts where id=%s returning *""",(str(id)))
    # deleted_post = cursor.fetchone()
    post_query = db.query(models.Post).filter(models.Post.id ==id)
    post = post_query.first()
    if post == None:
        raise HTTPException(status_code = status.HTTP_404_NOT_FOUND,
                            detail=f"post not found with id {id}"
                            )
    if post.owner_id != current_user.id:
        raise HTTPException(status_code=status.HTTP_403_FORBIDDEN,detail="not authoized to perform this action")

    post_query.delete(synchronize_session= False)
    db.commit()
    # conn.commit()
    return Response(status_code = status.HTTP_204_NO_CONTENT)
#################################################



############################################
@router.put("/{id}",response_model=schemas.Post)
def update_post(id:int, updated_post:schemas.PostCreate,db: Session = Depends(get_db),current_user:int = Depends(oauth2.get_current_user)):
    # cursor.execute("""update posts set title=%s, content=%s,published=%s where id=%s returning *""",(post.title,post.content,post.published,str(id)))
    # updated_post = cursor.fetchone()
    post_query = db.query(models.Post).filter(models.Post.id == id)
    post = post_query.first()
    if post == None:
        raise HTTPException(status_code = status.HTTP_404_NOT_FOUND,
                            detail = "post not found"
                                )
    if post.owner_id !=current_user.id:
        raise HTTPException(status_code=status.HTTP_403_FORBIDDEN,detail="not authorized to perform")
    post_query.update(updated_post.dict(),synchronize_session=False)
    db.commit()
    # conn.commit()
    return post_query.first()

##############################################
