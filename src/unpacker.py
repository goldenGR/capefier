from pathlib import Path
import zipfile

MC_PATH = "assets/skins/"

CAPES_TO_PATHS = [
  { "name": "Migrator", "path": "23/2340c0e03dd24a11b15a8b33c2a7e9e32abb2051b2481d0ba7defd635ca7a933" },
  { "name": "15th Anniversary", "path": "cd/cd9d82ab17fd92022dbd4a86cde4c382a7540e117fae7b9a2853658505a80625" },
  { "name": "Purple Heart", "path": "cb/cb40a92e32b57fd732a00fc325e7afb00a7ca74936ad50d8e860152e482cfbde" },
  { "name": "Realms Mapmaker", "path": "17/17912790ff164b93196f08ba71d0e62129304776d0f347334f8a6eae509f8a56" },
  { "name": "Minecon 2011", "path": "95/953cac8b779fe41383e675ee2b86071a71658f2180f56fbce8aa315ea70e2ed6" },
  { "name": "Minecon 2012", "path": "8a/8aa33788951727e898caff71bc70098d120b1f65d7ee4eed84d85e96cf351738" },
  { "name": "Minecon 2013", "path": "15/153b1a0dfcbae953cdeb6f2c2bf6bf79943239b1372780da44bcbb29273131da" },
  { "name": "Minecon 2015", "path": "b0/b0cc08840700447322d953a02b965f1d65a13a603bf64b17c803c21446fe1635" },
  { "name": "Minecon 2016", "path": "e7/e7dfea16dc83c97df01a12fabbd1216359c0cd0ea42f9999b6e97c584963e980" },
  { "name": "Minecraft Experience", "path": "76/7658c5025c77cfac7574aab3af94a46a8886e3b7722a895255fbf22ab8652434" },
  { "name": "Scrolls Champion", "path": "29/29bf0f478b2e089449a0b6216b5ee862383b007c599541a0a9100f378ad04047" },
  { "name": "Cobalt", "path": "4f/4fdbc899e4ca958d118223e9b1a2a1f59be5b36693cdd9dfcb5b624c4c8b13d8" },
  { "name": "Millionth Customer", "path": "70/70efffaf86fe5bc089608d3cb297d3e276b9eb7a8f9f2fe6659c23a2d8b18edf" },
  { "name": "dB", "path": "66/66b7361b97dd9b10080c627dea3109d7dabe20286ef64c396dfd3cc0d38b7ff0" },
  { "name": "Snowman", "path": "40/40155f104c0dc8cdeaadff2c44ab3a45ca306a3bcb8a66ef669f8d5426a5a2f3" },
  { "name": "Prismarine", "path": "d8/d8f8d13a1adf9636a16c31d47f3ecc9bb8d8533108aa5ad2a01b13b1a0c55eac" },
  { "name": "Turtle", "path": "50/5048ea61566353397247d2b7d946034de926b997d5e66c86483dfb1e031aee95" },
  { "name": "Birthday", "path": "33/336ae7f00f2154064f91190a131eee2251d51612d38bece47a497f96ebcfebb1" },
  { "name": "Valentine", "path": "45/45b8891ca563d5c774afad642fe3048c4147b347e970004ffa45a4ad0c64143b" },
  { "name": "Oxeye", "path": "ff/ffdec184ef9b53d0a8f7886922e9b4adb23d9963f1df6b34985b37bf07e7baba" },
  { "name": "Blueprint", "path": "15/15501578fe1dd925ccd322b2ff7045be36613085a13f11481ccb29486bae89dc" },
  { "name": "Vanilla", "path": "f9/f9a76537647989f9a0b6d001e320dac591c359e9e61a31f4ce11c88f207f0ad4" },
  { "name": "Pan", "path": "28/28de4a81688ad18b49e735a273e086c18f1e3966956123ccb574034c06f5d336" },
  { "name": "Common", "path": "5e/5ec930cdd2629c8771655c60eebeb867b4b6559b0e6d3bc71c40c96347fa03f0" },
  { "name": "Cherry Blossom", "path": "af/afd553b39358a24edfe3b8a9a939fa5fa4faa4d9a9c3d6af8eafb377fa05c2bb" },
  { "name": "Founder's", "path": "99/99aba02ef05ec6aa4d42db8ee43796d6cd50e4b2954ab29f0caeb85f96bf52a1" },
  { "name": "Copper", "path": "5e/5e6f3193e74cd16cdd6637d9bae5484e3a37ff2a14c2d157c659a07810b1bdca" },
  { "name": "Follower's", "path": "56/569b7f2a1d00d26f30efe3f9ab9ac817b1e6d35f4f3cfb0324ef2d328223d350" },
  { "name": "Home", "path": "1d/1de21419009db483900da6298a1e6cbf9f1bc1523a0dcdc16263fab150693edd" },
  { "name": "Menace", "path": "db/dbc21e222528e30dc88445314f7be6ff12d3aeebc3c192054fba7e3b3f8c77b1" },
  { "name": "Yearn", "path": "30/308b32a9e303155a0b4262f9e5483ad4a22e3412e84fe8385a0bdd73dc41fa89" },
  { "name": "Mojang Office", "path": "5c/5c29410057e32abec02d870ecb52ec25fb45ea81e785a7854ae8429d7236ca26" },
  { "name": "MCC 15th Year", "path": "56/56c35628fe1c4d59dd52561a3d03bfa4e1a76d397c8b9c476c2f77cb6aebb1df" },
  { "name": "Mojang Studios", "path": "9e/9e507afc56359978a3eb3e32367042b853cddd0995d17d0da995662913fb00f7" },
  { "name": "Mojira Moderator", "path": "ae/ae677f7d98ac70a533713518416df4452fe5700365c09cf45d0d156ea9396551" },
  { "name": "Spade", "path": "2e/2e002d5e1758e79ba51d08d92a0f3a95119f2f435ae7704916507b6c565a7da8" },
  { "name": "Mojang", "path": "57/5786fe99be377dfb6858859f926c4dbc995751e91cee373468c5fbf4865e7151" },
  { "name": "Mojang Classic", "path": "8f/8f120319222a9f4a104e2f5cb97b2cda93199a2ee9e1585cb8d09d6f687cb761" },
  { "name": "Zombie Horse", "path": "a3/a3f6e4f14801f3ea55e3d95b9b4ef3b5e8802d947f669de93d6ec4b9354a436b" },
  { "name": "Builder", "path": "2c/2c579968c64c1719740fd8c2a451461879b238002574fce48f7d1a7c36a1c7d4" },
  { "name": "Moonlight Trail", "path": "fe/fe8a02dfe9e390e44ff33d69feef9d3943f76d3901015bbd50f0b67722d288bd" },
  { "name": "Crafter", "path": "47/479eacefa3cdd7aca94207f36c0dd449653ddf259daf40544a5866baf05eee22" },
  { "name": "Translator", "path": "1b/1bf91499701404e21bd46b0191d63239a4ef76ebde88d27e4d430ac211df681e" },
  { "name": "Document", "path": "fd/fdcf48f01ec480d1d7cbec27f7ddce48c9da2be6724641109444dae58d4cd013" },
  { "name": "Translator Chinese", "path": "22/2262fb1d24912209490586ecae98aca8500df3eff91f2a07da37ee524e7e3cb6" },
  { "name": "Translator Japanese", "path": "ca/ca29f5dd9e94fb1748203b92e36b66fda80750c87ebc18d6eafdb0e28cc1d05f" },
  { "name": "Test", "path": "7a/7a93b1867eb599f2b76e6e1c30a0ddb530e6f4c7bce6515d1ba72b206df30e39" }
]

class CapePackManager:
    """Placeholder for actual pack logic. Wire this up to do real work."""

    def __init__(self):
        self.loaded_pack_path: Path | None = None
        self.files: list[object] = [] 

    def load_pack(self, path: str) -> list[zipfile.ZipExtFile]:
        self.loaded_pack_path = Path(path)
        with zipfile.ZipFile(path, "r") as zf:
            self.files = [zf.open(n) for n in zf.namelist() if not n.endswith("/")]
        return self.files

    def apply_pack(self, capes, capeEntry, target_dir: str) -> None:
        # raise NotImplementedError("apply_pack() not implemented yet")
        print("======= APPLY PACK =======")
        print(capeEntry)
        print("==========================")

        for cape in capes:
            cape_path = next(x["path"] for x in CAPES_TO_PATHS if x["name"] == cape)
            path = Path(target_dir) / MC_PATH / cape_path
            print(path)
            entry_dict = next(d for d in capeEntry if cape in d)
            capeContent = entry_dict[cape].read()

            path.parent.mkdir(parents=True, exist_ok=True)
            with open(path, "wb") as f:
                f.write(capeContent)