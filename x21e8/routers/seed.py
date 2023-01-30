from fastapi import APIRouter, HTTPException

from x21e8.wallet.utils import create_and_save_seed, save_seed_from_mnemonic

router = APIRouter(
    prefix="/seed",
    tags=["Seed"],
    responses={404: {"detail": "Not found"}},
)


@router.get("/", tags=["Seed"])
async def create_seed_and_provision(number_of_words: int):
    if number_of_words == 24:
        strength = 256
    elif number_of_words == 12:
        strength = 128
    else:
        raise HTTPException(status_code=420, detail="A mnemonic has to contain 12 or 24 words")
    return {"mnemonic": create_and_save_seed(strength)}


@router.post("/", tags=["Seed"])
async def recover_seed_from_mnemonic(mnemonic_phrase: str):
    word_array = mnemonic_phrase.split()
    size = len(word_array)
    if size not in [12, 24]:
        raise HTTPException(status_code=420, detail="A mnemonic has to contain 12 or 24 words")

    save_seed_from_mnemonic(mnemonic_phrase)
