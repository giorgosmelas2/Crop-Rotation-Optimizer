import random
from app.ml.core_models.crop import Crop
from app.ml.core_models.climate import Climate
from app.ml.core_models.field import Field
from app.ml.core_models.economics import Economics
from app.ml.core_models.farmer_knowledge import FarmerKnowledge
from app.models.rotation_input import RotationInfo, CropPair
from app.models.coordinates import Coordinates
from app.ml.grid.grid_utils import cell_create
from app.ml.grid.field_grid import FieldGrid
from app.agents.pest_agent import PestAgent
from app.agents.pest_simulation import PestSimulationManager

CROP_NAMES = [
    "Σκληρό σιτάρι",
    "Κριθάρι",
    "Αραβόσιτος",
    "Σόργος",
    "Ρύζι",
    "Βαμβάκι",
    "Ηλιοτρόπιο",
    "Ελαιόκαμβη",
    "Σουσάμι",
    "Κνήκος",
    "Σόγια",
    "Ρεβίθι",
    "Φακή",
    "Κούκι",
    "Κτηνοτροφικό μπιζέλι",
    "Μηδική",
    "Πατάτα",
    "Τομάτα",
    "Αγγούρι",
    "Καρπούζι",
    "Πεπόνι",
    "Πιπεριά",
    "Μελιτζάνα",
    "Κρεμμύδι",
    "Σκόρδο",
    "Καρότο",
    "Μαρούλι",
    "Σπανάκι",
    "Λάχανο",
    "Μπρόκολο",
    "Μαϊντανός",
    "Σέλινο",
    "Τσία",
    "Τεφ",
    "Κόκκινο τριφύλλι",
    "Λευκό τριφύλλι",
    "Λαθούρι",
    "Μοσχοσίταρο",
    "Κύμινο",
    "Σινάπι",
    "Ραπανάκι",
    "Αρακάς",
    "Κρεμμύδι χλωρό",
    "Φασόλι αναρυχώμενο",
    "Αλεξανδρινό τριφύλλι",
]

CROPS = [
    Crop(id=1,name='Σκληρό σιτάρι',family='Poaceae',order='Poales',is_legume=False,root_depth_cm=150,etc_mm=500,sow_month=11,harvest_month=6,t_min=5.0,t_max=32.0,t_opt_min=13.1,t_opt_max=23.9,rain_min_mm=350,rain_max_mm=600,ph_min=5.5,ph_max=8.0,g_min=180,g_max=220,n=13.0,p=2.4,k=3.5, soil_type='loam', residue_fraction=0.3 , n_fix=0.0, n_ret=3.9 ,p_ret=0.72 ,k_ret=1.05, pest='Hessian fly'),
    Crop(id=2,name='Κριθάρι',family='Poaceae',order='Poales',is_legume=False,root_depth_cm=120,etc_mm=450,sow_month=11,harvest_month=5,t_min=4.0,t_max=30.0,t_opt_min=11.8,t_opt_max=22.2,rain_min_mm=300,rain_max_mm=500,ph_min=5.5,ph_max=8.0,g_min=120,g_max=160,n=12.0,p=2.0,k=3.0, soil_type='loam', residue_fraction=0.3 , n_fix=0.0, n_ret=3.6 ,p_ret=0.6 ,k_ret=0.9, pest='Bird cherry-oat aphid'),
    Crop(id=3,name='Αραβόσιτος',family='Poaceae',order='Poales',is_legume=False,root_depth_cm=200,etc_mm=650,sow_month=4,harvest_month=9,t_min=10.0,t_max=45.0,t_opt_min=20.5,t_opt_max=34.5,rain_min_mm=500,rain_max_mm=800,ph_min=5.5,ph_max=7.8,g_min=110,g_max=150,n=25.0,p=5.0,k=10.0, soil_type='clay loam', residue_fraction=0.3 , n_fix=0.0, n_ret=7.5 ,p_ret=1.5 ,k_ret=3.0, pest='European corn borer'),
    Crop(id=4,name='Σόργος',family='Poaceae',order='Poales',is_legume=False,root_depth_cm=200,etc_mm=550,sow_month=5,harvest_month=10,t_min=12.0,t_max=33.0,t_opt_min=15.5,t_opt_max=25.5,rain_min_mm=600,rain_max_mm=1000,ph_min=6.0,ph_max=7.5,g_min=90,g_max=135,n=22.0,p=3.0,k=8.0, soil_type='clay loam', residue_fraction=0.3 , n_fix=0.0, n_ret=6.6 ,p_ret=0.9 ,k_ret=2.4, pest='Sugarcane aphid'),
    Crop(id=5,name='Ρύζι',family='Poaceae',order='Poales',is_legume=False,root_depth_cm=50,etc_mm=1000,sow_month=5,harvest_month=9,t_min=15.0,t_max=38.0,t_opt_min=21.9,t_opt_max=31.1,rain_min_mm=800,rain_max_mm=1200,ph_min=5.5,ph_max=7.5,g_min=120,g_max=160,n=20.0,p=4.0,k=5.0, soil_type='loamy clay', residue_fraction=0.3 , n_fix=0.0, n_ret=6.0 ,p_ret=1.2 , k_ret=1.5, pest='Black bean aphid'),
    Crop(id=6,name='Βαμβάκι',family='Malvaceae',order='Malvales',is_legume=False,root_depth_cm=200,etc_mm=600,sow_month=4,harvest_month=10,t_min=14.0,t_max=36.0,t_opt_min=18.0,t_opt_max=30.0,rain_min_mm=500,rain_max_mm=900,ph_min=5.5,ph_max=8.0,g_min=150,g_max=200,n=18.0,p=6.0,k=10.0, soil_type='clay loam', residue_fraction=0.2 , n_fix=0.0, n_ret=3.6 ,p_ret=1.2 ,k_ret=2.0, pest='Cotton bollworm'),
    Crop(id=7,name='Ηλιοτρόπιο',family='Asteraceae',order='Asterales',is_legume=False,root_depth_cm=200,etc_mm=800,sow_month=3,harvest_month=9,t_min=8.0,t_max=33.0,t_opt_min=15.5,t_opt_max=25.5,rain_min_mm=600,rain_max_mm=1000,ph_min=6.0,ph_max=7.5,g_min=90,g_max=130,n=15.0,p=5.0,k=12.0, soil_type='loamy clay', residue_fraction=0.3 , n_fix=0.0, n_ret=4.5 ,p_ret=1.5 ,k_ret=3.6, pest='Sunflower moth'),
    Crop(id=8,name='Ελαιόκαμβη',family='Brassicaceae',order='Brassicales',is_legume=False,root_depth_cm=150,etc_mm=550,sow_month=10,harvest_month=6,t_min=4.0,t_max=30.0,t_opt_min=11.8,t_opt_max=22.2,rain_min_mm=450,rain_max_mm=650,ph_min=5.5,ph_max=8.0,g_min=180,g_max=210,n=25.0,p=5.0,k=10.0, soil_type='clay loam', residue_fraction=0.25 , n_fix=0.0, n_ret=6.25 ,p_ret=1.25 ,k_ret=2.5, pest='Cabbage stem flea beetle'),
    Crop(id=9,name='Σουσάμι',family='Pedaliaceae',order='Lamiales',is_legume=False,root_depth_cm=150,etc_mm=500,sow_month=5,harvest_month=9,t_min=15.0,t_max=38.0,t_opt_min=21.9,t_opt_max=31.1,rain_min_mm=400,rain_max_mm=600,ph_min=5.5,ph_max=8.0,g_min=85,g_max=115,n=12.0,p=4.0,k=7.0, soil_type='loam', residue_fraction=0.3 , n_fix=0.0, n_ret=3.6 ,p_ret=1.2 ,k_ret=3.6, pest='Sesame webworm'),
    Crop(id=10,name='Κνήκος',family='Asteraceae',order='Asterales',is_legume=False,root_depth_cm=200,etc_mm=500,sow_month=11,harvest_month=6,t_min=5.0,t_max=32.0,t_opt_min=13.1,t_opt_max=23.9,rain_min_mm=400,rain_max_mm=600,ph_min=5.5,ph_max=8.0,g_min=120,g_max=150,n=15.0,p=3.0,k=9.0, soil_type='loam', residue_fraction=0.3 , n_fix=0.0, n_ret=4.5 ,p_ret=1.5 ,k_ret=3.6, pest='Safflower aphid'),
    Crop(id=11,name='Σόγια',family='Fabaceae',order='Fabales',is_legume=True,root_depth_cm=150,etc_mm=600,sow_month=5,harvest_month=9,t_min=10.0,t_max=35.0,t_opt_min=17.5,t_opt_max=27.5,rain_min_mm=500,rain_max_mm=700,ph_min=6.0,ph_max=7.5,g_min=110,g_max=150,n=0.0,p=4.0,k=10.0, soil_type='clay loam', residue_fraction=0.3 , n_fix=0.0, n_ret=4.5 ,p_ret=1.5 ,k_ret=3.6, pest='Soybean aphid'),
    Crop(id=12,name='Ρεβίθι',family='Fabaceae',order='Fabales',is_legume=True,root_depth_cm=100,etc_mm=425,sow_month=3,harvest_month=7,t_min=4.0,t_max=30.0,t_opt_min=11.8,t_opt_max=22.2,rain_min_mm=300,rain_max_mm=500,ph_min=6.0,ph_max=8.0,g_min=90,g_max=120,n=0.0,p=3.0,k=5.0, soil_type='loam', residue_fraction=0.3 , n_fix=0.0, n_ret=4.5 ,p_ret=1.5 ,k_ret=3.6, pest='Gram pod borer'),
    Crop(id=13,name='Φακή',family='Fabaceae',order='Fabales',is_legume=True,root_depth_cm=80,etc_mm=325,sow_month=12,harvest_month=6,t_min=3.0,t_max=28.0,t_opt_min=10.5,t_opt_max=20.5,rain_min_mm=250,rain_max_mm=400,ph_min=6.0,ph_max=8.0,g_min=90,g_max=130,n=0.0,p=2.5,k=4.0, soil_type='loam', residue_fraction=0.3 , n_fix=0.0, n_ret=4.1 ,p_ret=1.5 ,k_ret=3.6, pest='Pea aphid'),
    Crop(id=14,name='Κούκι',family='Fabaceae',order='Fabales',is_legume=True,root_depth_cm=120,etc_mm=475,sow_month=11,harvest_month=6,t_min=5.0,t_max=32.0,t_opt_min=13.1,t_opt_max=23.9,rain_min_mm=400,rain_max_mm=600,ph_min=6.0,ph_max=8.0,g_min=150,g_max=180,n=0.0,p=4.0,k=5.0, soil_type='loam', residue_fraction=0.3 , n_fix=0.0, n_ret=5.5 ,p_ret=1.2 ,k_ret=3.6, pest='Black bean aphid'),
    Crop(id=15,name='Κτηνοτροφικό μπιζέλι',family='Fabaceae',order='Fabales',is_legume=True,root_depth_cm=100,etc_mm=425,sow_month=11,harvest_month=6,t_min=5.0,t_max=32.0,t_opt_min=13.1,t_opt_max=23.9,rain_min_mm=300,rain_max_mm=500,ph_min=6.0,ph_max=7.5,g_min=90,g_max=120,n=0.0,p=3.0,k=4.0, soil_type='loam', residue_fraction=0.3 , n_fix=0.0, n_ret=2.0 ,p_ret=1.5 ,k_ret=3.6, pest='Pea weevil'),
    Crop(id=16,name='Μηδική',family='Fabaceae',order='Fabales',is_legume=True,root_depth_cm=300,etc_mm=900,sow_month=9,harvest_month=6,t_min=2.0,t_max=25.0,t_opt_min=10.0,t_opt_max=20.0,rain_min_mm=500,rain_max_mm=1000,ph_min=6.5,ph_max=8.0,g_min=70,g_max=90,n=0.0,p=5.0,k=15.0, soil_type='loamy clay', residue_fraction=0.3 , n_fix=0.0, n_ret=4.5 ,p_ret=2.5 ,k_ret=3.6, pest='Alfalfa weevil'),
    Crop(id=17,name='Πατάτα',family='Solanaceae',order='Solanales',is_legume=False,root_depth_cm=100,etc_mm=600,sow_month=2,harvest_month=6,t_min=5.0,t_max=30.0,t_opt_min=15.0,t_opt_max=25.0,rain_min_mm=350,rain_max_mm=600,ph_min=5.0,ph_max=6.5,g_min=75,g_max=120,n=20.0,p=5.0,k=25.0, soil_type='sandy loam', residue_fraction=0.3 , n_fix=0.0, n_ret=3.5 ,p_ret=1.5 ,k_ret=3.6, pest='Colorado potato beetle'),
    Crop(id=18,name='Τομάτα',family='Solanaceae',order='Solanales',is_legume=False,root_depth_cm=120,etc_mm=500,sow_month=3,harvest_month=7,t_min=6.0,t_max=32.0,t_opt_min=18.0,t_opt_max=28.0,rain_min_mm=400,rain_max_mm=700,ph_min=5.0,ph_max=7.0,g_min=90,g_max=120,n=25.0,p=6.0,k=20.0, soil_type='loam', residue_fraction=0.3 , n_fix=0.0, n_ret=2.5 ,p_ret=1.0 ,k_ret=3.2, pest='Tomato leaf miner'),
    Crop(id=19,name='Αγγούρι',family='Cucurbitaceae',order='Cucurbitales',is_legume=False,root_depth_cm=90,etc_mm=475,sow_month=4,harvest_month=7,t_min=10.0,t_max=30.0,t_opt_min=20.0,t_opt_max=30.0,rain_min_mm=300,rain_max_mm=600,ph_min=5.5,ph_max=7.5,g_min=50,g_max=70,n=20.0,p=5.0,k=20.0, soil_type='loam', residue_fraction=0.3 , n_fix=3.0, n_ret=4.5 ,p_ret=1.5 ,k_ret=3.6, pest='Cucumber beetle'),
    Crop(id=20,name='Καρπούζι',family='Cucurbitaceae',order='Cucurbitales',is_legume=False,root_depth_cm=150,etc_mm=500,sow_month=3,harvest_month=7,t_min=15.0,t_max=35.0,t_opt_min=25.0,t_opt_max=35.0,rain_min_mm=300,rain_max_mm=600,ph_min=5.5,ph_max=7.5,g_min=80,g_max=100,n=15.0,p=4.0,k=15.0, soil_type='loam', residue_fraction=0.3 , n_fix=5.0, n_ret=4.5 ,p_ret=1.5 ,k_ret=1.6, pest='Melon aphid'),
    Crop(id=21,name='Πεπόνι',family='Cucurbitaceae',order='Cucurbitales',is_legume=False,root_depth_cm=150,etc_mm=400,sow_month=3,harvest_month=7,t_min=15.0,t_max=33.0,t_opt_min=24.0,t_opt_max=32.0,rain_min_mm=250,rain_max_mm=500,ph_min=5.5,ph_max=7.5,g_min=75,g_max=95,n=15.0,p=4.0,k=13.0, soil_type='loam', residue_fraction=0.3 , n_fix=0.0, n_ret=4.5 ,p_ret=2.5 ,k_ret=1.6, pest='Melon aphid'),
    Crop(id=22,name='Πιπερία',family='Solanaceae',order='Solanales',is_legume=False,root_depth_cm=100,etc_mm=550,sow_month=2,harvest_month=8,t_min=10.0,t_max=34.0,t_opt_min=22.0,t_opt_max=30.0,rain_min_mm=300,rain_max_mm=650,ph_min=5.5,ph_max=7.0,g_min=90,g_max=120,n=25.0,p=6.0,k=18.0, soil_type='clay loam', residue_fraction=0.3 , n_fix=0.0, n_ret=4.0 ,p_ret=1.5 ,k_ret=3.4, pest='Pepper weevil'),
    Crop(id=23,name='Μελιτζάνα',family='Solanaceae',order='Solanales',is_legume=False,root_depth_cm=120,etc_mm=550,sow_month=2,harvest_month=9,t_min=12.0,t_max=30.0,t_opt_min=20.0,t_opt_max=28.0,rain_min_mm=300,rain_max_mm=700,ph_min=5.5,ph_max=7.5,g_min=100,g_max=140,n=20.0,p=5.0,k=15.0, soil_type='clay loam', residue_fraction=0.3 , n_fix=0.0, n_ret=4.5 ,p_ret=1.5 ,k_ret=2.5, pest='Eggplant fruit and shoot borer'),
    Crop(id=24,name='Κρεμμύδι',family='Amaryllidaceae',order='Asparagales',is_legume=False,root_depth_cm=60,etc_mm=450,sow_month=10,harvest_month=6,t_min=5.0,t_max=30.0,t_opt_min=12.0,t_opt_max=22.0,rain_min_mm=300,rain_max_mm=500,ph_min=6.0,ph_max=7.0,g_min=120,g_max=150,n=10.0,p=3.0,k=10.0, soil_type='loam', residue_fraction=0.3 , n_fix=0.0, n_ret=2.5 ,p_ret=1.5 ,k_ret=5.8, pest='Onion thrips'),
    Crop(id=25,name='Σκόρδο',family='Amaryllidaceae',order='Asparagales',is_legume=False,root_depth_cm=60,etc_mm=400,sow_month=11,harvest_month=6,t_min=5.0,t_max=32.0,t_opt_min=13.0,t_opt_max=23.0,rain_min_mm=300,rain_max_mm=500,ph_min=6.0,ph_max=7.5,g_min=180,g_max=210,n=8.0,p=2.5,k=8.0, soil_type='loam', residue_fraction=0.3 , n_fix=0.0, n_ret=4.5 ,p_ret=1.5 ,k_ret=3.6, pest='Onion thrips'),
    Crop(id=26,name='Καρότο',family='Apiaceae',order='Apiales',is_legume=False,root_depth_cm=60,etc_mm=300,sow_month=3,harvest_month=6,t_min=5.0,t_max=25.0,t_opt_min=15.0,t_opt_max=22.0,rain_min_mm=300,rain_max_mm=400,ph_min=5.5,ph_max=7.0,g_min=70,g_max=120,n=12.0,p=3.0,k=10.0, soil_type='loam', residue_fraction=0.4, n_fix=0.0, n_ret=4.3 ,p_ret=1.5 ,k_ret=3.6, pest='Carrot fly'),
    Crop(id=27,name='Μαρούλι',family='Asteraceae',order='Asterales',is_legume=False,root_depth_cm=45,etc_mm=500,sow_month=10,harvest_month=4,t_min=5.0,t_max=25.0,t_opt_min=17.0,t_opt_max=23.0,rain_min_mm=300,rain_max_mm=500,ph_min=6.0,ph_max=7.0,g_min=45,g_max=70,n=10.0,p=3.0,k=10.0, soil_type='loam', residue_fraction=0.4 , n_fix=5.0, n_ret=4.5 ,p_ret=1.5 ,k_ret=3.6, pest='Lettuce aphid'),
    Crop(id=28,name='Σπανάκι',family='Amaranthaceae',order='Caryophyllales',is_legume=False,root_depth_cm=45,etc_mm=450,sow_month=9,harvest_month=5,t_min=5.0,t_max=20.0,t_opt_min=15.0,t_opt_max=18.0,rain_min_mm=300,rain_max_mm=400,ph_min=6.0,ph_max=7.5,g_min=45,g_max=60,n=15.0,p=3.0,k=10.0, soil_type='loam', residue_fraction=0.4 , n_fix=0.0, n_ret=4.5 ,p_ret=1.5 ,k_ret=3.6, pest='Vegetable leafminer'),
    Crop(id=29,name='Λάχανο',family='Brassicaceae',order='Brassicales',is_legume=False,root_depth_cm=60,etc_mm=350,sow_month=9,harvest_month=5,t_min=5.0,t_max=22.0,t_opt_min=15.0,t_opt_max=20.0,rain_min_mm=250,rain_max_mm=500,ph_min=6.0,ph_max=7.5,g_min=80,g_max=150,n=15.0,p=4.0,k=15.0, soil_type='loam', residue_fraction=0.4 , n_fix=5.0, n_ret=4.5 ,p_ret=1.5 ,k_ret=3.6, pest='Diamondback moth'),
    Crop(id=30,name='Μπρόκολο',family='Brassicaceae',order='Brassicales',is_legume=False,root_depth_cm=90,etc_mm=500,sow_month=7,harvest_month=12,t_min=4.0,t_max=25.0,t_opt_min=10.3,t_opt_max=18.7,rain_min_mm=350,rain_max_mm=650,ph_min=6.0,ph_max=7.5,g_min=60,g_max=100,n=15.0,p=4.0,k=15.0, soil_type='loam', residue_fraction=0.4 , n_fix=5.0, n_ret=4.5 ,p_ret=1.5 ,k_ret=3.6, pest='Diamondback moth'),
    Crop(id=31, name='Ζαχαρότευλο', family='Amaranthaceae', order='Caryophyllales', is_legume=False, root_depth_cm=180, etc_mm=650, sow_month=3, harvest_month=10, t_min=5, t_max=30, t_opt_min=12.5, t_opt_max=22.5, rain_min_mm=550, rain_max_mm=750, ph_min=6.0, ph_max=8.0, g_min=180, g_max=220, n=15.0, p=4.0, k=20.0, soil_type='clay loam', residue_fraction=0.3, n_fix=0.0, n_ret=4.5, p_ret=1.2, k_ret=6.0, pest='Beet armyworm'),
    Crop(id=32, name='Βρώμη', family='Poaceae', order='Poales', is_legume=False, root_depth_cm=120, etc_mm=450, sow_month=11, harvest_month=6, t_min=4, t_max=30, t_opt_min=11.8, t_opt_max=22.2, rain_min_mm=300, rain_max_mm=600, ph_min=5.5, ph_max=7.5, g_min=120, g_max=160, n=12.0, p=2.0, k=3.0, soil_type='loam', residue_fraction=0.3, n_fix=0.0, n_ret=3.6, p_ret=0.6, k_ret=0.9, pest='Cereal aphid'),
    Crop(id=33, name='Σίκαλη', family='Poaceae', order='Poales', is_legume=False, root_depth_cm=150, etc_mm=450, sow_month=10, harvest_month=7, t_min=3, t_max=30, t_opt_min=11.1, t_opt_max=21.9, rain_min_mm=250, rain_max_mm=550, ph_min=5.5, ph_max=8.0, g_min=150, g_max=180, n=12.0, p=2.0, k=3.0, soil_type='loam', residue_fraction=0.3, n_fix=0.0, n_ret=3.6, p_ret=0.6, k_ret=0.9, pest='Cereal aphid'),
    Crop(id=34, name='Τριτικάλε', family='Poaceae', order='Poales', is_legume=False, root_depth_cm=150, etc_mm=450, sow_month=10, harvest_month=6, t_min=4, t_max=30, t_opt_min=11.8, t_opt_max=22.2, rain_min_mm=300, rain_max_mm=500, ph_min=5.5, ph_max=8.0, g_min=150, g_max=180, n=13.0, p=2.0, k=3.0, soil_type='loam', residue_fraction=0.3, n_fix=0.0, n_ret=3.9, p_ret=0.6, k_ret=0.9, pest='Cereal aphid'),
    Crop(id=35, name='Κέχρι', family='Poaceae', order='Poales', is_legume=False, root_depth_cm=122, etc_mm=462, sow_month=5, harvest_month=9, t_min=10, t_max=40, t_opt_min=21.5, t_opt_max=30.2, rain_min_mm=200, rain_max_mm=1000, ph_min=5.0, ph_max=7.5, g_min=60, g_max=120, n=17.5, p=3.7, k=9.0, soil_type='clay loam', residue_fraction=0.3, n_fix=0.0, n_ret=5.25, p_ret=1.11, k_ret=2.7, pest='Shoot fly'),
    Crop(id=36, name='Φαγόπυρος', family='Polygonaceae', order='Caryophyllales', is_legume=False, root_depth_cm=100, etc_mm=500, sow_month=4, harvest_month=8, t_min=7, t_max=30, t_opt_min=13.9, t_opt_max=23.1, rain_min_mm=450, rain_max_mm=750, ph_min=5.0, ph_max=6.5, g_min=70, g_max=90, n=8.0, p=2.0, k=3.0, soil_type='sandy loam', residue_fraction=0.3, n_fix=0.0, n_ret=2.4, p_ret=0.6, k_ret=0.9, pest='Buckwheat aphid'),
    Crop(id=37, name='Κινόα', family='Amaranthaceae', order='Caryophyllales', is_legume=False, root_depth_cm=120, etc_mm=500, sow_month=3, harvest_month=8, t_min=5, t_max=32, t_opt_min=13.1, t_opt_max=23.9, rain_min_mm=300, rain_max_mm=800, ph_min=5.5, ph_max=8.5, g_min=90, g_max=120, n=15.0, p=4.0, k=8.0, soil_type='clay loam', residue_fraction=0.3, n_fix=0.0, n_ret=4.5, p_ret=1.2, k_ret=2.4, pest='Quinoa aphid'),
    Crop(id=38, name='Αμάρανθος', family='Amaranthaceae', order='Caryophyllales', is_legume=False, root_depth_cm=150, etc_mm=550, sow_month=4, harvest_month=9, t_min=8, t_max=35, t_opt_min=16.1, t_opt_max=26.9, rain_min_mm=400, rain_max_mm=800, ph_min=5.0, ph_max=7.0, g_min=90, g_max=110, n=15.0, p=4.0, k=10.0, soil_type='clay loam', residue_fraction=0.3, n_fix=0.0, n_ret=4.5, p_ret=1.2, k_ret=3.0, pest='Amaranthus weevil'),
    Crop(id=39, name='Μαυρομάτικο φασόλι', family='Fabaceae', order='Fabales', is_legume=True, root_depth_cm=90, etc_mm=450, sow_month=5, harvest_month=9, t_min=12, t_max=35, t_opt_min=18.9, t_opt_max=28.1, rain_min_mm=400, rain_max_mm=700, ph_min=5.5, ph_max=6.8, g_min=70, g_max=85, n=0.0, p=3.0, k=3.0, soil_type='clay loam', residue_fraction=0.4, n_fix=5.0, n_ret=5.0, p_ret=1.2, k_ret=1.2, pest='Cotton bollworm'),
    Crop(id=40, name='Λούπινο', family='Fabaceae', order='Fabales', is_legume=True, root_depth_cm=150, etc_mm=500, sow_month=11, harvest_month=6, t_min=4, t_max=28, t_opt_min=11.2, t_opt_max=20.8, rain_min_mm=400, rain_max_mm=750, ph_min=4.5, ph_max=7.5, g_min=120, g_max=160, n=0.0, p=4.0, k=4.0, soil_type='clay loam', residue_fraction=0.4, n_fix=5.0, n_ret=5.0, p_ret=1.6, k_ret=1.6, pest='Lupin aphid'),
    Crop(id=41, name='Βίκος', family='Fabaceae', order='Fabales', is_legume=True, root_depth_cm=120, etc_mm=450, sow_month=10, harvest_month=5, t_min=3, t_max=28, t_opt_min=10.5, t_opt_max=20.5, rain_min_mm=350, rain_max_mm=600, ph_min=6.0, ph_max=8.0, g_min=110, g_max=140, n=0.0, p=4.0, k=4.0, soil_type='loam', residue_fraction=0.4, n_fix=5.0, n_ret=5.0, p_ret=1.6, k_ret=1.6, pest='Onion thrips'),
    Crop(id=42, name='Λιναρόσπορος', family='Linaceae', order='Malpighiales', is_legume=False, root_depth_cm=90, etc_mm=450, sow_month=10, harvest_month=7, t_min=8, t_max=32, t_opt_min=15.2, t_opt_max=24.8, rain_min_mm=300, rain_max_mm=600, ph_min=5.5, ph_max=7.5, g_min=90, g_max=120, n=15.0, p=5.0, k=8.0, soil_type='loam', residue_fraction=0.3, n_fix=0.0, n_ret=4.5, p_ret=1.5, k_ret=2.4, pest='Potato aphid'),
    Crop(id=43, name='Βιομηχανική κάνναβη', family='Cannabaceae', order='Rosales', is_legume=False, root_depth_cm=100, etc_mm=550, sow_month=4, harvest_month=9, t_min=5, t_max=35, t_opt_min=14.0, t_opt_max=26.0, rain_min_mm=300, rain_max_mm=700, ph_min=6.0, ph_max=7.5, g_min=90, g_max=110, n=20.0, p=5.0, k=15.0, soil_type='loam', residue_fraction=0.3, n_fix=0.0, n_ret=6.0, p_ret=1.5, k_ret=4.5, pest='Hemp russet mite'),
    Crop(id=44, name='Αράπικο φυστίκι', family='Fabaceae', order='Fabales', is_legume=True, root_depth_cm=100, etc_mm=650, sow_month=5, harvest_month=10, t_min=18, t_max=35, t_opt_min=23.1, t_opt_max=29.9, rain_min_mm=500, rain_max_mm=1000, ph_min=5.5, ph_max=7.0, g_min=120, g_max=160, n=0.0, p=5.0, k=7.0, soil_type='loamy clay', residue_fraction=0.4, n_fix=5.0, n_ret=5.0, p_ret=2.0, k_ret=2.8, pest='Peanut bud necrosis thrips'),
    Crop(id=45, name='Καμελίνα', family='Brassicaceae', order='Brassicales', is_legume=False, root_depth_cm=120, etc_mm=400, sow_month=10, harvest_month=7, t_min=4, t_max=30, t_opt_min=11.8, t_opt_max=22.2, rain_min_mm=300, rain_max_mm=450, ph_min=5.5, ph_max=7.5, g_min=85, g_max=100, n=15.0, p=4.0, k=9.0, soil_type='loam', residue_fraction=0.25, n_fix=0.0, n_ret=3.75, p_ret=1.0, k_ret=2.25, pest='Cabbage seedpod weevil'),
    Crop(id=46, name='Καπνός', family='Solanaceae', order='Solanales', is_legume=False, root_depth_cm=150, etc_mm=650, sow_month=3, harvest_month=8, t_min=15, t_max=34, t_opt_min=20.7, t_opt_max=28.3, rain_min_mm=600, rain_max_mm=800, ph_min=5.5, ph_max=6.5, g_min=100, g_max=140, n=25.0, p=5.0, k=25.0, soil_type='clay loam', residue_fraction=0.35, n_fix=0.0, n_ret=8.75, p_ret=1.75, k_ret=8.75, pest='Tobacco budworm'),
    Crop(id=47, name='Κολοκύθι', family='Cucurbitaceae', order='Cucurbitales', is_legume=False, root_depth_cm=60, etc_mm=450, sow_month=4, harvest_month=7, t_min=15, t_max=35, t_opt_min=21.0, t_opt_max=29.0, rain_min_mm=400, rain_max_mm=700, ph_min=6.0, ph_max=7.5, g_min=45, g_max=60, n=20.0, p=5.0, k=20.0, soil_type='clay loam', residue_fraction=0.3, n_fix=0.0, n_ret=6.0, p_ret=1.5, k_ret=6.0, pest='Squash vine borer'),
    Crop(id=48, name='Αγκινάρα', family='Asteraceae', order='Asterales', is_legume=False, root_depth_cm=90, etc_mm=650, sow_month=10, harvest_month=4, t_min=5, t_max=28, t_opt_min=11.9, t_opt_max=21.1, rain_min_mm=500, rain_max_mm=700, ph_min=6.5, ph_max=8.0, g_min=150, g_max=200, n=15.0, p=5.0, k=20.0, soil_type='clay loam', residue_fraction=0.3, n_fix=0.0, n_ret=4.5, p_ret=1.5, k_ret=6.0, pest='Artichoke plume moth'),
    Crop(id=49, name='Πράσο', family='Amaryllidaceae', order='Asparagales', is_legume=False, root_depth_cm=60, etc_mm=500, sow_month=2, harvest_month=11, t_min=5, t_max=25, t_opt_min=11.0, t_opt_max=19.0, rain_min_mm=400, rain_max_mm=600, ph_min=6.0, ph_max=7.5, g_min=90, g_max=130, n=15.0, p=4.0, k=15.0, soil_type='loam', residue_fraction=0.3, n_fix=0.0, n_ret=4.5, p_ret=1.2, k_ret=4.5, pest='Leek moth'),
    Crop(id=50, name='Πατζάρι', family='Amaranthaceae', order='Caryophyllales', is_legume=False, root_depth_cm=60, etc_mm=450, sow_month=3, harvest_month=7, t_min=4, t_max=25, t_opt_min=10.3, t_opt_max=18.7, rain_min_mm=350, rain_max_mm=500, ph_min=6.0, ph_max=7.0, g_min=60, g_max=90, n=12.0, p=5.0, k=18.0, soil_type='loam', residue_fraction=0.3, n_fix=0.0, n_ret=3.6, p_ret=1.5, k_ret=5.4, pest='Beet leaf miner'),
    Crop(id=51, name='Κόλιανδρος', family='Apiaceae', order='Apiales', is_legume=False, root_depth_cm=60, etc_mm=400, sow_month=2, harvest_month=6, t_min=10, t_max=30, t_opt_min=16.0, t_opt_max=24.0, rain_min_mm=300, rain_max_mm=600, ph_min=6.0, ph_max=7.5, g_min=90, g_max=120, n=10.0, p=4.0, k=8.0, soil_type='loam', residue_fraction=0.3, n_fix=0.0, n_ret=3.0, p_ret=1.2, k_ret=2.4, pest='Coriander aphid'),
    Crop(id=52, name='Άνηθος', family='Apiaceae', order='Apiales', is_legume=False, root_depth_cm=60, etc_mm=400, sow_month=2, harvest_month=5, t_min=6, t_max=28, t_opt_min=12.6, t_opt_max=21.4, rain_min_mm=300, rain_max_mm=500, ph_min=5.5, ph_max=7.5, g_min=70, g_max=100, n=10.0, p=4.0, k=8.0, soil_type='loam', residue_fraction=0.3, n_fix=0.0, n_ret=3.0, p_ret=1.2, k_ret=2.4, pest='Carrot fly'),
    Crop(id=53, name='Μάραθος', family='Apiaceae', order='Apiales', is_legume=False, root_depth_cm=90, etc_mm=450, sow_month=2, harvest_month=7, t_min=10, t_max=30, t_opt_min=16.0, t_opt_max=24.0, rain_min_mm=300, rain_max_mm=600, ph_min=6.0, ph_max=7.5, g_min=90, g_max=130, n=15.0, p=4.0, k=10.0, soil_type='loam', residue_fraction=0.3, n_fix=0.0, n_ret=4.5, p_ret=1.2, k_ret=3.0, pest='European seed bug'),
    Crop(id=54, name='Ρίγανη', family='Lamiaceae', order='Lamiales', is_legume=False, root_depth_cm=50, etc_mm=450, sow_month=3, harvest_month=7, t_min=5, t_max=30, t_opt_min=12.5, t_opt_max=22.5, rain_min_mm=300, rain_max_mm=700, ph_min=6.0, ph_max=8.0, g_min=90, g_max=120, n=10.0, p=4.0, k=12.0, soil_type='loam', residue_fraction=0.3, n_fix=0.0, n_ret=3.0, p_ret=1.2, k_ret=3.6, pest='Citrus spittlebug'),
    Crop(id=55, name='Βασιλικός', family='Lamiaceae', order='Lamiales', is_legume=False, root_depth_cm=50, etc_mm=450, sow_month=4, harvest_month=7, t_min=10, t_max=35, t_opt_min=17.5, t_opt_max=27.5, rain_min_mm=400, rain_max_mm=600, ph_min=5.5, ph_max=7.5, g_min=60, g_max=80, n=15.0, p=5.0, k=15.0, soil_type='loam', residue_fraction=0.3, n_fix=0.0, n_ret=4.5, p_ret=1.5, k_ret=4.5, pest='Japanese beetle'),
    Crop(id=56, name='Μαιντανός', family='Apiaceae', order='Apiales', is_legume=False, root_depth_cm=60, etc_mm=400, sow_month=2, harvest_month=7, t_min=4, t_max=28, t_opt_min=11.2, t_opt_max=20.8, rain_min_mm=300, rain_max_mm=500, ph_min=6.0, ph_max=7.0, g_min=70, g_max=90, n=15.0, p=4.0, k=10.0, soil_type='loam', residue_fraction=0.3, n_fix=0.0, n_ret=4.5, p_ret=1.2, k_ret=3.0, pest='Celery leaf miner'),
    Crop(id=57, name='Σέλινο', family='Apiaceae', order='Apiales', is_legume=False, root_depth_cm=60, etc_mm=500, sow_month=2, harvest_month=7, t_min=8, t_max=24, t_opt_min=12.8, t_opt_max=19.2, rain_min_mm=400, rain_max_mm=600, ph_min=6.0, ph_max=7.0, g_min=120, g_max=150, n=20.0, p=5.0, k=20.0, soil_type='loam', residue_fraction=0.3, n_fix=0.0, n_ret=6.0, p_ret=1.5, k_ret=6.0, pest='Celery leaf miner'),
    Crop(id=58, name='Τσία', family='Lamiaceae', order='Lamiales', is_legume=False, root_depth_cm=100, etc_mm=500, sow_month=4, harvest_month=9, t_min=11, t_max=36, t_opt_min=18.5, t_opt_max=28.5, rain_min_mm=400, rain_max_mm=800, ph_min=6.0, ph_max=7.5, g_min=100, g_max=120, n=15.0, p=4.0, k=10.0, soil_type='clay loam', residue_fraction=0.3, n_fix=0.0, n_ret=4.5, p_ret=1.2, k_ret=3.0, pest='Lygus bug'),
    Crop(id=59, name='Τεφ', family='Poaceae', order='Poales', is_legume=False, root_depth_cm=150, etc_mm=500, sow_month=5, harvest_month=9, t_min=10, t_max=35, t_opt_min=17.5, t_opt_max=27.5, rain_min_mm=300, rain_max_mm=600, ph_min=5.0, ph_max=7.5, g_min=80, g_max=120, n=12.0, p=3.0, k=8.0, soil_type='loam', residue_fraction=0.3, n_fix=0.0, n_ret=3.6, p_ret=0.9, k_ret=2.4, pest='Shoot fly'),
    Crop(id=60, name='Κόκκινο τριφύλλι', family='Fabaceae', order='Fabales', is_legume=True, root_depth_cm=160, etc_mm=600, sow_month=3, harvest_month=8, t_min=4, t_max=28, t_opt_min=11.2, t_opt_max=20.8, rain_min_mm=450, rain_max_mm=800, ph_min=6.0, ph_max=7.2, g_min=90, g_max=120, n=0.0, p=3.0, k=12.0, soil_type='clay loam', residue_fraction=0.4, n_fix=5.0, n_ret=5.0, p_ret=1.2, k_ret=4.8, pest='Clover root curculio'),
    Crop(id=61, name='Λευκό τριφύλλι', family='Fabaceae', order='Fabales', is_legume=True, root_depth_cm=50, etc_mm=650, sow_month=3, harvest_month=9, t_min=5, t_max=27, t_opt_min=11.6, t_opt_max=20.4, rain_min_mm=550, rain_max_mm=1000, ph_min=6.0, ph_max=7.2, g_min=90, g_max=120, n=0.0, p=3.0, k=12.0, soil_type='loamy clay', residue_fraction=0.4, n_fix=5.0, n_ret=5.0, p_ret=1.2, k_ret=4.8, pest='Clover root curculio'),
    Crop(id=62, name='Λαθούρι', family='Fabaceae', order='Fabales', is_legume=True, root_depth_cm=100, etc_mm=400, sow_month=11, harvest_month=6, t_min=3, t_max=32, t_opt_min=11.7, t_opt_max=23.3, rain_min_mm=250, rain_max_mm=450, ph_min=5.5, ph_max=8.0, g_min=85, g_max=120, n=0.0, p=3.0, k=3.0, soil_type='loam', residue_fraction=0.4, n_fix=5.0, n_ret=5.0, p_ret=1.2, k_ret=1.2, pest='Pea aphid'),
    Crop(id=63, name='Μοσχοσίταρο', family='Fabaceae', order='Fabales', is_legume=True, root_depth_cm=90, etc_mm=400, sow_month=11, harvest_month=4, t_min=5, t_max=30, t_opt_min=12.5, t_opt_max=22.5, rain_min_mm=300, rain_max_mm=600, ph_min=6.0, ph_max=7.5, g_min=90, g_max=120, n=0.0, p=3.0, k=3.0, soil_type='loam', residue_fraction=0.4, n_fix=5.0, n_ret=5.0, p_ret=1.2, k_ret=1.2, pest='Cowpea aphid'),
    Crop(id=64, name='Κύμινο', family='Apiaceae', order='Apiales', is_legume=False, root_depth_cm=60, etc_mm=400, sow_month=11, harvest_month=6, t_min=5, t_max=35, t_opt_min=14.0, t_opt_max=26.0, rain_min_mm=200, rain_max_mm=500, ph_min=6.0, ph_max=7.5, g_min=110, g_max=140, n=15.0, p=4.0, k=12.0, soil_type='loam', residue_fraction=0.3, n_fix=0.0, n_ret=4.5, p_ret=1.2, k_ret=3.6, pest='Cumin aphid'),
    Crop(id=65, name='Σινάπι', family='Brassicaceae', order='Brassicales', is_legume=False, root_depth_cm=90, etc_mm=450, sow_month=11, harvest_month=5, t_min=5, t_max=30, t_opt_min=12.5, t_opt_max=22.5, rain_min_mm=300, rain_max_mm=450, ph_min=5.5, ph_max=8.0, g_min=90, g_max=120, n=20.0, p=5.0, k=15.0, soil_type='loam', residue_fraction=0.25, n_fix=0.0, n_ret=5.0, p_ret=1.25, k_ret=3.75, pest='Mustard aphid'),
    Crop(id=66, name='Ραπανάκι', family='Brassicaceae', order='Brassicales', is_legume=False, root_depth_cm=50, etc_mm=400, sow_month=2, harvest_month=4, t_min=4, t_max=28, t_opt_min=11.2, t_opt_max=20.8, rain_min_mm=300, rain_max_mm=500, ph_min=6.0, ph_max=7.5, g_min=30, g_max=60, n=10.0, p=3.0, k=10.0, soil_type='loam', residue_fraction=0.25, n_fix=0.0, n_ret=2.5, p_ret=0.75, k_ret=2.5, pest='Flea beetle'),
    Crop(id=67, name='Αρακάς', family='Fabaceae', order='Fabales', is_legume=True, root_depth_cm=100, etc_mm=400, sow_month=11, harvest_month=5, t_min=5, t_max=28, t_opt_min=12.0, t_opt_max=20.0, rain_min_mm=300, rain_max_mm=700, ph_min=6.0, ph_max=7.5, g_min=130, g_max=170, n=0.0, p=4.0, k=8.0, soil_type='loam', residue_fraction=0.4, n_fix=5.0, n_ret=5.0, p_ret=1.6, k_ret=3.2, pest='Pea weevil'),
    Crop(id=68, name='Κρεμμύδι χλωρό', family='Amaryllidaceae', order='Asparagales', is_legume=False, root_depth_cm=25, etc_mm=400, sow_month=11, harvest_month=3, t_min=10, t_max=28, t_opt_min=15.0, t_opt_max=22.0, rain_min_mm=300, rain_max_mm=600, ph_min=6.0, ph_max=7.5, g_min=70, g_max=90, n=12.0, p=6.0, k=8.0, soil_type='loam', residue_fraction=0.3, n_fix=0.0, n_ret=3.6, p_ret=1.8, k_ret=2.4, pest='Onion thrips'),
    Crop(id=69, name='Φασόλι αναρυχώμενο', family='Fabaceae', order='Fabales', is_legume=True, root_depth_cm=80, etc_mm=500, sow_month=3, harvest_month=7, t_min=8, t_max=28, t_opt_min=16.0, t_opt_max=24.0, rain_min_mm=500, rain_max_mm=900, ph_min=6.0, ph_max=7.5, g_min=100, g_max=130, n=0.0, p=5.0, k=8.0, soil_type='clay loam', residue_fraction=0.4, n_fix=5.0, n_ret=5.0, p_ret=2.0, k_ret=3.2, pest='Bean pod borerne'),
    Crop(id=70, name='Αλεξανδρινό τριφύλλι', family='Fabaceae', order='Fabales', is_legume=True, root_depth_cm=70, etc_mm=500, sow_month=10, harvest_month=5, t_min=10, t_max=30, t_opt_min=18.0, t_opt_max=24.0, rain_min_mm=400, rain_max_mm=800, ph_min=6.0, ph_max=7.5, g_min=180, g_max=240, n=0.0, p=4.0, k=6.0, soil_type='clay loam', residue_fraction=0.4, n_fix=5.0, n_ret=5.0, p_ret=1.6, k_ret=2.4, pest='Clover root curculio'),
]

PEST_AGENTS = [
    PestAgent(name='Hessian fly', affected_crops=['Σκληρό σιτάρι'], affected_families=['Poaceae'], affected_orders=['Poales']),
    PestAgent(name='Bird cherry-oat aphid', affected_crops=['Κριθάρι'], affected_families=['Poaceae'], affected_orders=['Poales']),
    PestAgent(name='Eggplant fruit and shoot borer', affected_crops=['Αραβόσιτος', 'Μελιτζάνα'], affected_families=['Poaceae', 'Solanaceae'], affected_orders=['Poales', 'Solanales']),
    PestAgent(name='Sugarcane aphid', affected_crops=['Σόργος'], affected_families=['Poaceae'], affected_orders=['Poales']),
    PestAgent(name='Brown planthopper', affected_crops=['Ρύζι'], affected_families=['Poaceae'], affected_orders=['Poales']),
    PestAgent(name='Cotton bollworm', affected_crops=['Βαμβάκι', 'Μαυρομάτικο φασόλι'], affected_families=['Malvaceae', 'Fabaceae'], affected_orders=['Malvales', 'Fabales']),
    PestAgent(name='Sunflower moth', affected_crops=['Ηλιοτρόπιο'], affected_families=['Asteraceae'], affected_orders=['Asterales']),
    PestAgent(name='Cabbage stem flea beetle', affected_crops=['Ελαιόκαμβη'], affected_families=['Brassicaceae'], affected_orders=['Brassicales']),
    PestAgent(name='Sesame webworm', affected_crops=['Σουσάμι'], affected_families=['Pedaliaceae'], affected_orders=['Lamiales']),
    PestAgent(name='Safflower aphid', affected_crops=['Κνήκος'], affected_families=['Asteraceae'], affected_orders=['Asterales']),
    PestAgent(name='Soybean aphid', affected_crops=['Σόγια'], affected_families=['Asteraceae'], affected_orders=['Asterales']),
    PestAgent(name='Gram pod borer', affected_crops=['Ρεβίθι'], affected_families=['Fabaceae'], affected_orders=['Fabales']),
    PestAgent(name='Pea aphid', affected_crops=['Φακή','Λαθούρι'], affected_families=['Fabaceae'], affected_orders=['Fabales']),
    PestAgent(name='Black bean aphid', affected_crops=['Κούκι'], affected_families=['Fabaceae'], affected_orders=['Fabales']),
    PestAgent(name='Pea weevil', affected_crops=['Κτηνοτροφικό μπιζέλι', 'Αρακάς'], affected_families=['Fabaceae'], affected_orders=['Fabales']),
    PestAgent(name='Alfalfa weevil', affected_crops=['Μηδική'], affected_families=['Fabaceae'], affected_orders=['Fabales']),
    PestAgent(name='Colorado potato beetle', affected_crops=['Πατάτα'], affected_families=['Solanaceae'], affected_orders=['Solanales']),
    PestAgent(name='Tomato leaf miner', affected_crops=['Τομάτα'], affected_families=['Solanaceae'], affected_orders=['Solanales']),
    PestAgent(name='Cucumber beetle', affected_crops=['Αγγούρι'], affected_families=['Cucurbitaceae'], affected_orders=['Cucurbitales']),
    PestAgent(name='Melon aphid', affected_crops=['Καρπούζι', 'Πεπόνι'], affected_families=['Cucurbitaceae'], affected_orders=['Cucurbitales']),
    PestAgent(name='Pepper weevil', affected_crops=['Πιπερία'], affected_families=['Solanaceae'], affected_orders=['Solanales']),
    PestAgent(name='Onion thrips', affected_crops=['Κρεμμύδι', 'Σκόρδο', 'Βίκος','Κρεμμύδι χλωρό'], affected_families=['Amaryllidaceae', 'Fabaceae'], affected_orders=['Asparagales', 'Fabales']),
    PestAgent(name='Carrot fly', affected_crops=['Καρότο', 'Άνηθος'], affected_families=['Apiaceae'], affected_orders=['Apiales']),
    PestAgent(name='Lettuce aphid', affected_crops=['Μαρούλι'], affected_families=['Asteraceae'], affected_orders=['Asterales']),
    PestAgent(name='Vegetable leafminer', affected_crops=['Σπανάκι'], affected_families=['Amaranthaceae'], affected_orders=['Caryophyllales']),
    PestAgent(name='Diamondback moth', affected_crops=['Λάχανο', 'Μπρόκολο'], affected_families=['Brassicaceae'], affected_orders=['Brassicales']),
    PestAgent(name='Beet armyworm', affected_crops=['Ζαχαρότευλο'], affected_families=['Amaranthaceae'], affected_orders=['Caryophyllales']),
    PestAgent(name='Cereal aphid', affected_crops=['Βρώμη', 'Σίκαλη', 'Τριτικάλε'], affected_families=['Poaceae'], affected_orders=['Poales']),
    PestAgent(name='Shoot fly', affected_crops=['Φαγόπυρος', 'Τεφ'], affected_families=['Polygonaceae', 'Poaceae'], affected_orders=['Caryophyllales', 'Poales']),
    PestAgent(name='Quinoa aphid', affected_crops=['Κινόα'], affected_families=['Amaranthaceae'], affected_orders=['Caryophyllales']),
    PestAgent(name='Amaranthus weevil', affected_crops=['Αμάρανθος'], affected_families=['Amaranthaceae'], affected_orders=['Caryophyllales']),
    PestAgent(name='Lupin aphid', affected_crops=['Λούπινο'], affected_families=['Fabaceae'], affected_orders=['Fabales']),
    PestAgent(name='Potato aphid', affected_crops=['Λιναρόσπορος'], affected_families=['Linaceae'], affected_orders=['Malpighiales']),
    PestAgent(name='Hemp russet mite', affected_crops=['Βιομηχανική κάνναβη'], affected_families=['Cannabaceae'], affected_orders=['Rosales']),
    PestAgent(name='Peanut bud necrosis thrip', affected_crops=['Αράπικο φυστίκι'], affected_families=['Fabaceae'], affected_orders=['Fabales']),
    PestAgent(name='Cabbage seedpod weevil', affected_crops=['Καμελίνα'], affected_families=['Brassicaceae'], affected_orders=['Brassicales']),
    PestAgent(name='Tobacco budworm', affected_crops=['Καπνός'], affected_families=['Solanaceae'], affected_orders=['Solanales']),
    PestAgent(name='Squash vine borer', affected_crops=['Κολοκύθι'], affected_families=['Cucurbitaceae'], affected_orders=['Cucurbitales']), 
    PestAgent(name='Artichoke plume moth', affected_crops=['Αγκινάρα'], affected_families=['Asteraceae'], affected_orders=['Asterales']),
    PestAgent(name='Leek moth', affected_crops=['Πράσο'], affected_families=['Amaryllidaceae'], affected_orders=['Asparagales']),
    PestAgent(name='Beet leaf miner', affected_crops=['Πατζάρι'], affected_families=['Amaranthaceae'], affected_orders=['Caryophyllales']),
    PestAgent(name='Coriander aphid', affected_crops=['Κόλιανδρος'], affected_families=['Apiaceae'], affected_orders=['Apiales']),
    PestAgent(name='European seed bug', affected_crops=['Μάραθος'], affected_families=['Apiaceae'], affected_orders=['Apiales']),
    PestAgent(name='Citrus spittlebug', affected_crops=['Ρίγανη'], affected_families=['Lamiaceae'], affected_orders=['Lamiales']),
    PestAgent(name='Japanese beetle', affected_crops=['Βασιλικός'], affected_families=['Lamiaceae'], affected_orders=['Lamiales']),
    PestAgent(name='Celery leaf miner', affected_crops=['Μαιντανός', 'Σέλινο'], affected_families=['Apiaceae'], affected_orders=['Apiales']),
    PestAgent(name='Lygus bug', affected_crops=['Τσία'], affected_families=['Lamiaceae'], affected_orders=['Lamiales']), 
    PestAgent(name='Clover root curculio', affected_crops=['Κόκκινο τριφύλλι', 'Λευκό τριφύλλι', 'Αλεξανδρινό τριφύλλι'], affected_families=['Fabaceae'], affected_orders=['Fabales']),
    PestAgent(name='Cowpea aphid', affected_crops=['Μοσχοσίταρο'], affected_families=['Fabaceae'], affected_orders=['Poales']),
    PestAgent(name='Cumin aphid', affected_crops=['Κύμινο'], affected_families=['Apiaceae'], affected_orders=['Apiales']),
    PestAgent(name='Mustard aphid', affected_crops=['Σινάπι'], affected_families=['Brassicaceae'], affected_orders=['Brassicales']),
    PestAgent(name='Flea beetle', affected_crops=['Ραπανάκι'], affected_families=['Brassicaceae'], affected_orders=['Brassicales']), 
    PestAgent(name='Bean pod borerne', affected_crops=['Φασόλι αναρυχώμενο'], affected_families=['Fabaceae'], affected_orders=['Fabales'])
]

PEST_DICT = {p.name: p for p in PEST_AGENTS}

unique_machinery = [
    "Τρακτέρ",
    "Αλέτρι",
    "Δισκοσβάρνα",
    "Ψεκαστικό",
    "Σπαρτική",
    "Θεριζοαλωνιστική",
    "Λιπασματοδιανομέας",
    "Καλλιεργητής",
    "Καλαμποκοσυλλεκτική",
    "Σύστημα άρδευσης",
    "Φρέζα",
    "Χορτοσυλλεκτικό",
    "Χορτοκοπτικό (κοπτικό δίσκου ή μπάρας)",
    "Πατατοφυτευτική",
    "Πατατοσυλλεκτική",
    "Φυτευτική μηχανή",
    "Συλλεκτικό μηχάνημα για κρεμμύδια",
    "Μηχάνημα εκρίζωσης σκόρδων",
    "Συλλεκτική μηχανή καρότων",
    "Χειρωνακτική συγκομιδή",
    "Εξαλακωτής",
    "Συγκομιστική μηχανή τεύτλων",
    "Θεριζοαλωνιστική (hempseed)",
    "Μεταφορικό μέσω (hempseed)",
    "Θεριστική μπάρας ή κοπτικό μηχάνημα (fiber)",
    "Μηχανή εναπόθεσης (fiber)",
    "Μηχανή συμπίεσης ή δεματοποίησης (fiber)",
    "Αναστροφέας",
    "Συγκομιστική μηχανή φιστικιών",
    "Φυτευτική Καπνού",
    "Καλλιεργητής (ή καλλιεργητής με φρέζα)",
    "Κοπτικό Καπνού",
    "Αποξηραντήριο",
    "Χορτοκοπτικό μηχάνημα"
]



def random_dummy_climate():
    return Climate(
        monthly_tmin=[
            random.uniform(0, 6),     
            random.uniform(1, 7),    
            random.uniform(4, 9),    
            random.uniform(8, 12),   
            random.uniform(12, 17),   
            random.uniform(17, 22),   
            random.uniform(20, 25),   
            random.uniform(20, 25),   
            random.uniform(16, 21),  
            random.uniform(12, 17),  
            random.uniform(7, 12),   
            random.uniform(3, 8)     
        ],
        monthly_tmax=[
            random.uniform(10, 14),   
            random.uniform(11, 15),   
            random.uniform(14, 19),   
            random.uniform(18, 23),   
            random.uniform(23, 28),  
            random.uniform(28, 33),   
            random.uniform(32, 38),   
            random.uniform(32, 38),  
            random.uniform(27, 32),   
            random.uniform(21, 26),   
            random.uniform(15, 20),   
            random.uniform(11, 16)    
        ],
        monthly_rain=[
            random.randint(60, 120),  
            random.randint(50, 100), 
            random.randint(40, 90),   
            random.randint(30, 70),   
            random.randint(10, 40),   
            random.randint(0, 25),    
            random.randint(0, 20), 
            random.randint(0, 20),    
            random.randint(10, 40),  
            random.randint(30, 80),   
            random.randint(50, 100), 
            random.randint(60, 120)   
        ],
        monthly_evap=[
            random.uniform(30, 50),    
            random.uniform(35, 55),    
            random.uniform(50, 80),   
            random.uniform(60, 90),    
            random.uniform(90, 130),   
            random.uniform(110, 150),  
            random.uniform(130, 180), 
            random.uniform(120, 160),  
            random.uniform(90, 130),   
            random.uniform(60, 90),    
            random.uniform(40, 70),   
            random.uniform(30, 60)     
        ],
        monthly_rh=[
            random.uniform(0.7, 0.9),   
            random.uniform(0.65, 0.85),
            random.uniform(0.6, 0.8),
            random.uniform(0.55, 0.75),
            random.uniform(0.5, 0.7),
            random.uniform(0.4, 0.6),
            random.uniform(0.3, 0.5),
            random.uniform(0.35, 0.55),
            random.uniform(0.45, 0.65),
            random.uniform(0.55, 0.75),
            random.uniform(0.6, 0.8),
            random.uniform(0.65, 0.85)  
        ]
    )


def random_dummy_field():
    rotation_info = random_dummy_rotation_info()
    cells = cell_create(rotation_info)
    field_grid = FieldGrid(cells=cells)
    return Field(
        total_area=12.0,
        grid=field_grid 
    )

def random_dummy_rotation_info():
    return RotationInfo(
        user_id="",
        crops=["Σιτάρι", "Λούπινο"],
        coordinates=Coordinates(lat=39.0, lng=22.0),
        area=12.0,
        soil_type="loamy",
        irrigation=random.choice([0, 1, 2, 3]),
        fertilization=random.choice([0, 1, 2, 3]),
        spraying=random.choice([0, 1, 2, 3]),
        n=random.uniform(5.0, 80.0),
        p=random.uniform(3.0, 15.0),
        k=random.uniform(2.0, 25.0),
        ph=random.uniform(5.5, 8.5),
        machinery=["Θεριζοαλωνιστική"],
        past_crops=["Βαμβάκι", "Καλαμπόκι"],
        effective_pairs=[CropPair(crop1="Σιτάρι", crop2="Λούπινο", value=1)],
        uneffective_pairs=[CropPair(crop1="Βαμβάκι", crop2="Ρύζι", value=-1)],
        years=3
    )


def random_dummy_years():
    return random.randint(3, 10)


def random_dummy_farmer_knowledge():
    eff_len = random.randint(1, 4)
    unEff_len = random.randint(1,4)

    effective_pairs = []
    uneffective_pairs = []

    for _ in range(eff_len):
        crop1 = random.choice(CROP_NAMES)
        crop2 = random.choice(CROP_NAMES)
        value = random.randint(1,3)

        while crop1 == crop2:
            crop2 = random.choice(CROP_NAMES)
        
        pair = CropPair(crop1=crop1, crop2=crop2, value=value)
        effective_pairs.append(pair)

    for _ in range(unEff_len):
        crop1 = random.choice(CROP_NAMES)
        crop2 = random.choice(CROP_NAMES)
        value = random.randint(1,3)

        while crop1 == crop2:
            crop2 = random.choice(CROP_NAMES)
        
        pair = CropPair(crop1=crop1, crop2=crop2, value=value)
        uneffective_pairs.append(pair)
    
    return FarmerKnowledge(
        effective_pairs=effective_pairs,
        uneffective_pairs=uneffective_pairs,
        past_crops=[]
    )
    


def random_dummy_beneficial_rotations():
    num_rotations = random.randint(1, 5)
    beneficial_rotations = []
    for _ in range(num_rotations):
        rotation_len = random.randint(2, 5)
        rotation = []
        for _ in range(rotation_len):
            crop = random.choice(CROP_NAMES)
            rotation.append(crop)
        
        beneficial_rotations.append(rotation)


    return beneficial_rotations


def random_dummy_missing_machinery():
    num_missing = random.randint(1,4)
    missing_machinery = []

    for _ in range(num_missing):
        machinery = random.choice(unique_machinery)
        while machinery in missing_machinery:
            machinery = random.choice(unique_machinery)
        missing_machinery.append(machinery)

    return missing_machinery


def random_dummy_past_crops():
    crop1 = random.choice(CROP_NAMES)
    crop2 = random.choice(CROP_NAMES)
    return [crop1, crop2]


def dummy_economic_data():
    return {
        1: Economics(crop_id=1, tonne_price_sell=338.5, unit_price=0.8, units_per_acre=22.0, kg_yield_per_acre=400),
        2: Economics(crop_id=2, tonne_price_sell=191.6, unit_price=2.5, units_per_acre=12.0, kg_yield_per_acre=720),
        3: Economics(crop_id=3, tonne_price_sell=293.8, unit_price=66.7, units_per_acre=2.5, kg_yield_per_acre=1000),
        4: Economics(crop_id=4, tonne_price_sell=250.0, unit_price=3.6, units_per_acre=3.0, kg_yield_per_acre=11000),
        5: Economics(crop_id=5, tonne_price_sell=325.1, unit_price=1.6, units_per_acre=16.0, kg_yield_per_acre=830),
        6: Economics(crop_id=6, tonne_price_sell=1550.0, unit_price=5.45, units_per_acre=3.0, kg_yield_per_acre=400),
        7: Economics(crop_id=7, tonne_price_sell=440.0, unit_price=10.0, units_per_acre=0.5, kg_yield_per_acre=500),
        8: Economics(crop_id=8, tonne_price_sell=430.0, unit_price=8.0, units_per_acre=1.5, kg_yield_per_acre=400),
        9: Economics(crop_id=9, tonne_price_sell=2300.0, unit_price=7.0, units_per_acre=1.5, kg_yield_per_acre=250),
        10: Economics(crop_id=10, tonne_price_sell=800.0, unit_price=4.0, units_per_acre=3.3, kg_yield_per_acre=800),
        11: Economics(crop_id=11, tonne_price_sell=400.0, unit_price=3.0, units_per_acre=8.0, kg_yield_per_acre=500),
        12: Economics(crop_id=12, tonne_price_sell=2282.7, unit_price=5.0, units_per_acre=10.0, kg_yield_per_acre=280),
        13: Economics(crop_id=13, tonne_price_sell=2216.3, unit_price=3.2, units_per_acre=12.0, kg_yield_per_acre=200),
        14: Economics(crop_id=14, tonne_price_sell=640.0, unit_price=15.0, units_per_acre=15.0, kg_yield_per_acre=3000),
        15: Economics(crop_id=15, tonne_price_sell=285.0, unit_price=0.9, units_per_acre=80.0, kg_yield_per_acre=5000),
        16: Economics(crop_id=16, tonne_price_sell=1500.0, unit_price=2.5, units_per_acre=20.0, kg_yield_per_acre=1000),
        17: Economics(crop_id=17, tonne_price_sell=900.0, unit_price=5.0, units_per_acre=4.0, kg_yield_per_acre=800),
        18: Economics(crop_id=18, tonne_price_sell=1200.0, unit_price=3.0, units_per_acre=10.0, kg_yield_per_acre=600),
        19: Economics(crop_id=19, tonne_price_sell=200.0, unit_price=1.0, units_per_acre=50.0, kg_yield_per_acre=7000),
        20: Economics(crop_id=20, tonne_price_sell=340.0, unit_price=0.7, units_per_acre=100.0, kg_yield_per_acre=6000),
        21: Economics(crop_id=21, tonne_price_sell=800.0, unit_price=15.0, units_per_acre=2.0, kg_yield_per_acre=1500),
        22: Economics(crop_id=22, tonne_price_sell=950.0, unit_price=2.0, units_per_acre=30.0, kg_yield_per_acre=2000),
        23: Economics(crop_id=23, tonne_price_sell=720.0, unit_price=4.5, units_per_acre=6.0, kg_yield_per_acre=1200),
        24: Economics(crop_id=24, tonne_price_sell=420.0, unit_price=0.6, units_per_acre=150.0, kg_yield_per_acre=5500),
        25: Economics(crop_id=25, tonne_price_sell=880.0, unit_price=8.0, units_per_acre=5.0, kg_yield_per_acre=900),
        26: Economics(crop_id=26, tonne_price_sell=650.0, unit_price=3.0, units_per_acre=12.0, kg_yield_per_acre=700),
        27: Economics(crop_id=27, tonne_price_sell=400.0, unit_price=2.0, units_per_acre=25.0, kg_yield_per_acre=2500),
        28: Economics(crop_id=28, tonne_price_sell=1100.0, unit_price=6.0, units_per_acre=4.0, kg_yield_per_acre=1100),
        29: Economics(crop_id=29, tonne_price_sell=600.0, unit_price=1.5, units_per_acre=40.0, kg_yield_per_acre=3000),
        30: Economics(crop_id=30, tonne_price_sell=480.0, unit_price=2.2, units_per_acre=18.0, kg_yield_per_acre=1800),
        31: Economics(crop_id=31, tonne_price_sell=1050.0, unit_price=10.0, units_per_acre=3.0, kg_yield_per_acre=1000),
        32: Economics(crop_id=32, tonne_price_sell=300.0, unit_price=0.5, units_per_acre=75.0, kg_yield_per_acre=6000),
        33: Economics(crop_id=33, tonne_price_sell=1250.0, unit_price=7.0, units_per_acre=2.0, kg_yield_per_acre=800),
        34: Economics(crop_id=34, tonne_price_sell=520.0, unit_price=1.2, units_per_acre=30.0, kg_yield_per_acre=2500),
        35: Economics(crop_id=35, tonne_price_sell=610.0, unit_price=3.5, units_per_acre=20.0, kg_yield_per_acre=1500),
        36: Economics(crop_id=36, tonne_price_sell=295.0, unit_price=1.0, units_per_acre=60.0, kg_yield_per_acre=4000),
        37: Economics(crop_id=37, tonne_price_sell=1020.0, unit_price=9.0, units_per_acre=2.0, kg_yield_per_acre=750),
        38: Economics(crop_id=38, tonne_price_sell=820.0, unit_price=4.0, units_per_acre=5.0, kg_yield_per_acre=900),
        39: Economics(crop_id=39, tonne_price_sell=720.0, unit_price=2.5, units_per_acre=12.0, kg_yield_per_acre=1300),
        40: Economics(crop_id=40, tonne_price_sell=380.0, unit_price=0.8, units_per_acre=80.0, kg_yield_per_acre=4500),
        41: Economics(crop_id=41, tonne_price_sell=280.0, unit_price=0.6, units_per_acre=90.0, kg_yield_per_acre=5000),
        42: Economics(crop_id=42, tonne_price_sell=520.0, unit_price=1.8, units_per_acre=50.0, kg_yield_per_acre=2200),
        43: Economics(crop_id=43, tonne_price_sell=650.0, unit_price=2.2, units_per_acre=35.0, kg_yield_per_acre=1700),
        44: Economics(crop_id=44, tonne_price_sell=780.0, unit_price=7.0, units_per_acre=2.0, kg_yield_per_acre=800),
        45: Economics(crop_id=45, tonne_price_sell=430.0, unit_price=2.5, units_per_acre=30.0, kg_yield_per_acre=1400),
        46: Economics(crop_id=46, tonne_price_sell=950.0, unit_price=5.0, units_per_acre=8.0, kg_yield_per_acre=600),
        47: Economics(crop_id=47, tonne_price_sell=610.0, unit_price=3.0, units_per_acre=12.0, kg_yield_per_acre=1000),
        48: Economics(crop_id=48, tonne_price_sell=340.0, unit_price=1.0, units_per_acre=60.0, kg_yield_per_acre=3000),
        49: Economics(crop_id=49, tonne_price_sell=780.0, unit_price=6.0, units_per_acre=4.0, kg_yield_per_acre=1200),
        50: Economics(crop_id=50, tonne_price_sell=890.0, unit_price=7.5, units_per_acre=2.5, kg_yield_per_acre=900),
        51: Economics(crop_id=51, tonne_price_sell=1020.0, unit_price=8.0, units_per_acre=3.5, kg_yield_per_acre=1000),
        52: Economics(crop_id=52, tonne_price_sell=660.0, unit_price=4.0, units_per_acre=15.0, kg_yield_per_acre=1800),
        53: Economics(crop_id=53, tonne_price_sell=430.0, unit_price=2.0, units_per_acre=25.0, kg_yield_per_acre=1500),
        54: Economics(crop_id=54, tonne_price_sell=950.0, unit_price=5.0, units_per_acre=10.0, kg_yield_per_acre=800),
        55: Economics(crop_id=55, tonne_price_sell=330.0, unit_price=1.0, units_per_acre=100.0, kg_yield_per_acre=6000),
        56: Economics(crop_id=56, tonne_price_sell=720.0, unit_price=3.5, units_per_acre=20.0, kg_yield_per_acre=1400),
        57: Economics(crop_id=57, tonne_price_sell=1400.0, unit_price=0.08, units_per_acre=6000.0, kg_yield_per_acre=5000),
        58: Economics(crop_id=58, tonne_price_sell=2500.0, unit_price=12.0, units_per_acre=0.6, kg_yield_per_acre=117),
        59: Economics(crop_id=59, tonne_price_sell=2000.0, unit_price=10.0, units_per_acre=1.5, kg_yield_per_acre=90),
        60: Economics(crop_id=60, tonne_price_sell=280.0, unit_price=5.0, units_per_acre=0.5, kg_yield_per_acre=3500),
        61: Economics(crop_id=61, tonne_price_sell=280.0, unit_price=5.0, units_per_acre=0.5, kg_yield_per_acre=3500),
        62: Economics(crop_id=62, tonne_price_sell=650.0, unit_price=1.4, units_per_acre=10.0, kg_yield_per_acre=100),
        63: Economics(crop_id=63, tonne_price_sell=1300.0, unit_price=4.0, units_per_acre=5.0, kg_yield_per_acre=600),
        64: Economics(crop_id=64, tonne_price_sell=1900.0, unit_price=500.0, units_per_acre=1.5, kg_yield_per_acre=200),
        65: Economics(crop_id=65, tonne_price_sell=700.0, unit_price=50.0, units_per_acre=0.4, kg_yield_per_acre=300),
        66: Economics(crop_id=66, tonne_price_sell=600.0, unit_price=40.0, units_per_acre=2.5, kg_yield_per_acre=2500),
        67: Economics(crop_id=67, tonne_price_sell=500.0, unit_price=15.0, units_per_acre=15.0, kg_yield_per_acre=1000),
        68: Economics(crop_id=68, tonne_price_sell=350.0, unit_price=90.0, units_per_acre=0.8, kg_yield_per_acre=8000),
        69: Economics(crop_id=69, tonne_price_sell=950.0, unit_price=26.0, units_per_acre=12.0, kg_yield_per_acre=3000),
        70: Economics(crop_id=70, tonne_price_sell=280.0, unit_price=5.0, units_per_acre=0.5, kg_yield_per_acre=3500),
    }


def dummy_crops_required_machinery():
    return {
        1: ['Τρακτέρ', 'Αλέτρι', 'Δισκοσβάρνα', 'Ψεκαστικό', 'Σπαρτική', 'Θεριζοαλωνιστική', 'Λιπασματοδιανομέας'],
        2: ['Τρακτέρ', 'Αλέτρι', 'Δισκοσβάρνα', 'Σπαρτική', 'Θεριζοαλωνιστική', 'Ψεκαστικό', 'Λιπασματοδιανομέας'],
        3: ['Τρακτέρ', 'Καλλιεργητής', 'Δισκοσβάρνα', 'Σπαρτική', 'Καλαμποκοσυλλεκτική'],
        4: ['Τρακτέρ', 'Καλλιεργητής', 'Δισκοσβάρνα', 'Σπαρτική', 'Θεριζοαλωνιστική', 'Λιπασματοδιανομέας', 'Ψεκαστικό'],
        5: ['Τρακτέρ', 'Καλλιεργητής', 'Σπαρτική', 'Δισκοσβάρνα', 'Σύστημα άρδευσης', 'Θεριζοαλωνιστική', 'Φρέζα', 'Ψεκαστικό'],
        6: ['Τρακτέρ', 'Καλλιεργητής', 'Δισκοσβάρνα', 'Σπαρτική', 'Λιπασματοδιανομέας', 'Ψεκαστικό', 'Βαμβακοσυλλεκτική'],
        7: ['Τρακτέρ', 'Καλλιεργητής', 'Δισκοσβάρνα', 'Σπαρτική', 'Θεριζοαλωνιστική', 'Λιπασματοδιανομέας'],
        8: ['Τρακτέρ', 'Καλλιεργητής', 'Δισκοσβάρνα', 'Σπαρτική', 'Λιπασματοδιανομέας', 'Ψεκαστικό', 'Θεριζοαλωνιστική'],
        9: ['Τρακτέρ', 'Καλλιεργητής', 'Δισκοσβάρνα', 'Σπαρτική', 'Λιπασματοδιανομέας', 'Ψεκαστικό', 'Θεριζοαλωνιστική' ],
        10: ['Τρακτέρ', 'Καλλιεργητής', 'Δισκοσβάρνα', 'Σπαρτική', 'Θεριζοαλωνιστική', 'Λιπασματοδιανομέας'],
        11: ['Τρακτέρ', 'Καλλιεργητής', 'Σπαρτική', 'Λιπασματοδιανομέας', 'Ψεκαστικό', 'Θεριζοαλωνιστική', 'Δισκοσβάρνα'],
        12: ['Τρακτέρ', 'Καλλιεργητής', 'Σπαρτική', 'Λιπασματοδιανομέας', 'Ψεκαστικό', 'Θεριζοαλωνιστική', 'Δισκοσβάρνα'],
        13: ['Τρακτέρ', 'Καλλιεργητής', 'Σπαρτική', 'Λιπασματοδιανομέας', 'Ψεκαστικό', 'Θεριζοαλωνιστική'],
        14: ['Τρακτέρ', 'Καλλιεργητής', 'Δισκοσβάρνα', 'Σπαρτική', 'Θεριζοαλωνιστική', 'Λιπασματοδιανομέας', 'Ψεκαστικό'],
        15: ['Τρακτέρ', 'Καλλιεργητής', 'Δισκοσβάρνα', 'Σπαρτική', 'Λιπασματοδιανομέας', 'Ψεκαστικό', 'Θεριζοαλωνιστική'],
        16: ['Τρακτέρ', 'Καλλιεργητής', 'Δισκοσβάρνα',  'Σπαρτική', 'Λιπασματοδιανομέας', 'Ψεκαστικό', 'Χορτοσυλλεκτικό', 'Χορτοκοπτικό (κοπτικό δίσκου ή μπάρας)'],
        17: ['Τρακτέρ', 'Φρεζοκαλλιεργητής', 'Πατατοφυτευτική', 'Λιπασματοδιανομέας', 'Ψεκαστικό', 'Πατατοσυλλεκτική'],
        18: ['Τρακτέρ', 'Φρέζα', 'Φυτευτική μηχανή', 'Λιπασματοδιανομέας', 'Ψεκαστικό', 'Σύστημα άρδευσης'],
        19: ['Τρακτέρ', 'Φρέζα', 'Φυτευτική μηχανή', 'Λιπασματοδιανομέας', 'Ψεκαστικό', 'Σύστημα άρδευσης '],
        20: ['Τρακτέρ', 'Φρέζα', 'Φυτευτική μηχανή', 'Λιπασματοδιανομέας', 'Ψεκαστικό', 'Σύστημα άρδευσης'],
        21: ['Τρακτέρ', 'Φρέζα', 'Φυτευτική μηχανή', 'Λιπασματοδιανομέας', 'Ψεκαστικό', 'Σύστημα άρδευσης'],
        22: ['Τρακτέρ', 'Φρέζα', 'Φυτευτική μηχανή', 'Λιπασματοδιανομέας', 'Ψεκαστικό', 'Σύστημα άρδευσης'],
        23: ['Τρακτέρ', 'Φρέζα', 'Φυτευτική μηχανή', 'Λιπασματοδιανομέας', 'Ψεκαστικό', 'Σύστημα άρδευσης'],
        24: ['Τρακτέρ', 'Φρέζα', 'Σπαρτική', 'Λιπασματοδιανομέας', 'Ψεκαστικό', 'Σύστημα άρδευσης', 'Συλλεκτικό μηχάνημα για κρεμμύδια'],
        25: ['Τρακτέρ', 'Φρέζα', 'Φυτευτική μηχανή', 'Λιπασματοδιανομέας', 'Ψεκαστικό', 'Σύστημα άρδευσης', 'Μηχάνημα εκρίζωσης σκόρδων'],
        26: ['Τρακτέρ', 'Φρέζα', 'Σπαρτική', 'Λιπασματοδιανομέας', 'Ψεκαστικό', 'Σύστημα άρδευσης', 'Συλλεκτική μηχανή καρότων'],
        27: ['Τρακτέρ', 'Φρέζα', 'Φυτευτική μηχανή', 'Λιπασματοδιανομέας', 'Ψεκαστικό', 'Σύστημα άρδευσης', 'Χειρωνακτική συγκομιδή'],
        28: ['Τρακτέρ', 'Φρέζα', 'Σπαρτική', 'Λιπασματοδιανομέας', 'Ψεκαστικό', 'Σύστημα άρδευσης', 'Χειρωνακτική συγκομιδή'],
        29: ['Τρακτέρ', 'Φρέζα', 'Φυτευτική μηχανή', 'Λιπασματοδιανομέας', 'Ψεκαστικό', 'Σύστημα άρδευσης', 'Χειρωνακτική συγκομιδή'],
        30: ['Τρακτέρ', 'Φρέζα', 'Φυτευτική μηχανή', 'Λιπασματοδιανομέας', 'Ψεκαστικό', 'Σύστημα άρδευσης', 'Χειρωνακτική συγκομιδή'],
        31: ['Τρακτέρ', 'Καλλιεργητής', 'Δισκοσβάρνα', 'Σπαρτική', 'Λιπασματοδιανομέας', 'Ψεκαστικό', 'Σύστημα άρδευσης', 'Εξαλακωτής', 'Συγκομιστική μηχανή τεύτλων'],
        32: ['Τρακτέρ', 'Καλλιεργητής', 'Σπαρτική', 'Λιπασματοδιανομέας', 'Ψεκαστικό', 'Θεριζοαλωνιστική'],
        33: ['Τρακτέρ', 'Καλλιεργητής', 'Δισκοσβάρνα', 'Σπαρτική', 'Λιπασματοδιανομέας', 'Ψεκαστικό', 'Θεριζοαλωνιστική'],
        34: ['Τρακτέρ', 'Καλλιεργητής', 'Σπαρτική', 'Λιπασματοδιανομέας', 'Ψεκαστικό', 'Θεριζοαλωνιστική'],
        35: ['Τρακτέρ', 'Καλλιεργητής', 'Δισκοσβάρνα', 'Σπαρτική', 'Λιπασματοδιανομέας', 'Ψεκαστικό', 'Θεριζοαλωνιστική'],
        36: ['Τρακτέρ', 'Καλλιεργητής', 'Δισκοσβάρνα', 'Σπαρτική', 'Λιπασματοδιανομέας', 'Ψεκαστικό', 'Θεριζοαλωνιστική'],
        37: ['Τρακτέρ', 'Καλλιεργητής', 'Δισκοσβάρνα', 'Σπαρτική', 'Λιπασματοδιανομέας', 'Ψεκαστικό', 'Θεριζοαλωνιστική'],
        38: ['Τρακτέρ', 'Φρέζα', 'Σπαρτική', 'Λιπασματοδιανομέας', 'Ψεκαστικό', 'Θεριζοαλωνιστική'],
        39: ['Τρακτέρ', 'Καλλιεργητής', 'Δισκοσβάρνα', 'Σπαρτική', 'Λιπασματοδιανομέας', 'Ψεκαστικό', 'Θεριζοαλωνιστική'],
        40: ['Τρακτέρ', 'Καλλιεργητής', 'Δισκοσβάρνα', 'Σπαρτική', 'Λιπασματοδιανομέας', 'Θεριζοαλωνιστική'],
        41: ['Τρακτέρ', 'Καλλιεργητής', 'Δισκοσβάρνα', 'Σπαρτική', 'Λιπασματοδιανομέας', 'Χειρωνακτική συγκομιδή'],
        42: ['Τρακτέρ', 'Καλλιεργητής', 'Δισκοσβάρνα', 'Σπαρτική', 'Λιπασματοδιανομέας', 'Ψεκαστικό', 'Θεριζοαλωνιστική'],
        43: ['Τρακτέρ', 'Φρέζα', 'Σπαρτική', 'Λιπασματοδιανομέας', 'Ψεκαστικό', 'Θεριζοαλωνιστική (hempseed)', 'Μεταφορικό μέσω (hempseed)', 'Θεριστική μπάρας ή κοπτικό μηχάνημα (fiber)', 'Μηχανή εναπόθεσης (fiber)', 'Μηχανή συμπίεσης ή δεματοποίησης (fiber)'],
        44: ['Τρακτέρ', 'Φρέζα', 'Σπαρτική', 'Λιπασματοδιανομέας', 'Ψεκαστικό', 'Αναστροφέας', 'Συγκομιστική μηχανή φιστικιών', 'Χειρωνακτική συγκομιδή'],
        45: ['Τρακτέρ', 'Φρέζα', 'Σπαρτική', 'Λιπασματοδιανομέας', 'Ψεκαστικό', 'Θεριζοαλωνιστική'],
        46: ['Τρακτέρ', 'Φυτευτική Καπνού', 'Καλλιεργητής', 'Κοπτικό Καπνού', 'Αποξηραντήριο', 'Χειρωνακτική συγκομιδή'],
        47: ['Τρακτέρ', 'Φρέζα', 'Φυτευτική μηχανή', 'Λιπασματοδιανομέας', 'Ψεκαστικό', 'Σύστημα άρδευσης', 'Χειρωνακτική συγκομιδή'],
        48: ['Τρακτέρ', 'Φρέζα', 'Φυτευτική μηχανή', 'Λιπασματοδιανομέας', 'Ψεκαστικό', 'Σύστημα άρδευσης', 'Χειρωνακτική συγκομιδή'],
        49: ['Τρακτέρ', 'Φρέζα', 'Φυτευτική μηχανή', 'Λιπασματοδιανομέας', 'Ψεκαστικό', 'Σύστημα άρδευσης', 'Χειρωνακτική συγκομιδή'],
        50: ['Τρακτέρ', 'Φρέζα', 'Σπαρτική', 'Λιπασματοδιανομέας', 'Ψεκαστικό', 'Σύστημα άρδευσης', 'Χειρωνακτική συγκομιδή'],
        51: ['Τρακτέρ', 'Φρέζα', 'Δισκοσβάρνα', 'Σπαρτική', 'Λιπασματοδιανομέας', 'Θεριζοαλωνιστική', 'Χειρωνακτική συγκομιδή', 'Σύστημα άρδευσης'],
        52: ['Τρακτέρ', 'Φρέζα', 'Σπαρτική', 'Λιπασματοδιανομέας', 'Σύστημα άρδευσης', 'Χειρωνακτική συγκομιδή'],
        53: ['Τρακτέρ', 'Φρέζα', 'Σπαρτική', 'Λιπασματοδιανομέας', 'Σύστημα άρδευσης', 'Θεριζοαλωνιστική', 'Χειρωνακτική συγκομιδή'], 
        54: ['Τρακτέρ', 'Δισκοσβάρνα', 'Καλλιεργητής', 'Σπαρτική', 'Λιπασματοδιανομέας', 'Σύστημα άρδευσης', 'Χειρωνακτική συγκομιδή'],
        55: ['Τρακτέρ', 'Φρέζα', 'Σπαρτική', 'Λιπασματοδιανομέας', 'Σύστημα άρδευσης', 'Θεριζοαλωνιστική', 'Χειρωνακτική συγκομιδή'],
        56: ['Τρακτέρ', 'Φρέζα', 'Σπαρτική', 'Λιπασματοδιανομέας', 'Ψεκαστικό', 'Σύστημα άρδευσης', 'Χειρωνακτική συγκομιδή'],
        57: ['Τρακτέρ', 'Φρέζα', 'Φυτευτική μηχανή', 'Ψεκαστικό', 'Λιπασματοδιανομέας', 'Σύστημα άρδευσης', 'Θεριζοαλωνιστική', 'Χειρωνακτική συγκομιδή'],
        58: ['Τρακτέρ',  'Φρέζα', 'Σπαρτική', 'Λιπασματοδιανομέας' , 'Θεριζοαλωνιστική'],
        59: ['Τρακτέρ', 'Αλέτρι', 'Δισκοσβάρνα', 'Σπαρτική', 'Ψεκαστικό', 'Σύστημα άρδευσης', 'Θεριζοαλωνιστική'],
        60: ['Τρακτέρ', 'Φρέζα' ,'Σπαρτική', 'Λιπασματοδιανομέας',' Σύστημα άρδευσης', 'Χορτοκοπτικό μηχάνημα'],
        61: ['Τρακτέρ', 'Φρέζα' ,'Σπαρτική', 'Λιπασματοδιανομέας', 'Σύστημα άρδευσης', 'Χορτοκοπτικό μηχάνημα'],
        62: ['Τρακτέρ', 'Καλλιεργητής', 'Δισκοσβάρνα', 'Σπαρτική', 'Λιπασματοδιανομέας', 'Σύστημα άρδευσης', 'Θεριζοαλωνιστική'],
        63: ['Τρακτέρ', 'Καλλιεργητής' , 'Σπαρτική', 'Λιπασματοδιανομέας', 'Θεριζοαλωνιστική'],
        64: ['Τρακτέρ', 'Φρέζα', 'Δισκοσβάρνα', 'Σπαρτική', 'Χειρωνακτική συγκομιδή'],
        65: ['Τρακτέρ', 'καλλιεργητής', 'Δισκοσβάρνα', 'Σπαρτική', 'Θεριζοαλωνιστική', 'Λιπασματοδιανομέας'],
        66: ['Τρακτέρ', 'Φρέζα', 'Σπαρτική', 'Λιπασματοδιανομέας',  'Σύστημα άρδευσης', 'Χειρωνακτική συγκομιδή'],
        67: ['Τρακτέρ', 'Φρέζα' ,'Σπαρτική', 'Λιπασματοδιανομέας', 'Σύστημα άρδευσης', 'Θεριζοαλωνιστική', 'Χειρωνακτική συγκομιδή'],
        68: ['Τρακτέρ', 'Φρέζα' ,'Σπαρτική', 'Λιπασματοδιανομέας', 'Σύστημα άρδευσης', 'Χειρωνακτική συγκομιδή'],
        69: ['Τρακτέρ', 'Φρέζα' , 'Σπαρτική', 'Λιπασματοδιανομέας', 'Σύστημα άρδευσης', 'Ψεκαστικό', 'Χειρωνακτική συγκομιδή'],
        70: ['Τρακτέρ', 'Φρέζα' ,'Σπαρτική', 'Λιπασματοδιανομέας', 'Σύστημα άρδευσης', 'Χορτοκοπτικό μηχάνημα']
    }

def random_dummy_crops():
    rand_num = random.randint(20, 70)
    random_crops = random.sample(CROPS, rand_num)
    return random_crops

def dummy_pest_agents(random_crops): 
    seen = set()
    pests = []

    for crop in random_crops:
        pest = PEST_DICT.get(crop.pest)
        if pest and pest.name not in seen:
            pests.append(pest)
            seen.add(pest.name)

    return pests
    
def dummy_past_pest_agents(random_past_crops):
    seen = set()
    past_pests = []
    for agent in PEST_AGENTS:
        if any(c in agent.affected_crops for c in random_past_crops):
            if agent.name not in seen:
                past_pests.append(agent)
                seen.add(agent.name)
    return past_pests

def dummy_pest_manager(pest_agents, past_pests):
    return PestSimulationManager(
        pest_agents=pest_agents, 
        past_pest_agents=past_pests   
    )