from fastapi import APIRouter

# this tell that this file is not an application
# we will add these routes in the main file from where they can be reachable
router = APIRouter()

@router.get('/auth/')
async def get_user():
    return {'user':'authenticated'}