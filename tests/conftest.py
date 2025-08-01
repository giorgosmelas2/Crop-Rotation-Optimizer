import pytest
import random
from app.models.rotation_input import RotationInfo
from app.models.coordinates import Coordinates
from app.ml.core_models.crop import Crop
from app.ml.core_models.field import Field
from app.ml.core_models.climate import Climate
from app.ml.grid.cell import Cell
from app.ml.grid.field_grid import FieldGrid
from app.ml.core_models.farmer_knowledge import FarmerKnowledge
from app.models.rotation_input import CropPair
from app.ml.core_models.economics import Economics
from app.ml.grid.grid_utils import cell_create
from app.agents.pest_agent import PestAgent
from app.agents.pest_simulation import PestSimulationManager

# Crops
@pytest.fixture
def dummy_crop():
    return Crop(
        id=1,
        name="Σιτάρι",
        family="Poaceae",
        order="Poales",
        is_legume=False,
        root_depth_cm=100,
        etc_mm=200,
        sow_month=10,
        harvest_month=4,
        t_min=5, 
        t_max=30, 
        t_opt_min=12, 
        t_opt_max=25,
        rain_min_mm=300, 
        rain_max_mm=700,
        ph_min=6, 
        ph_max=7.5,
        g_min=90, 
        g_max=150,
        n=120, 
        p=30, 
        k=40,
        soil_type="loamy",
        residue_fraction=0.2,
        n_fix=0, 
        n_ret=36, 
        p_ret=6, 
        k_ret=8,
        pest="Hessian fly"
    )

def make_dummy_crop(**overrides) -> Crop:
    defaults = {
        "id": 1,
        "name": "Generic Crop",
        "family": "Testaceae",
        "order": "Testales",
        "is_legume": False,
        "root_depth_cm": 100,
        "etc_mm": 400,
        "sow_month": 10,
        "harvest_month": 5,
        "t_min": 5.0,
        "t_max": 35.0,
        "t_opt_min": 15.0,
        "t_opt_max": 25.0,
        "rain_min_mm": 200,
        "rain_max_mm": 600,
        "ph_min": 6.0,
        "ph_max": 7.5,
        "g_min": 90,
        "g_max": 150,
        "n": 120.0,
        "p": 30.0,
        "k": 40.0,
        "soil_type": "loamy",
        "residue_fraction": 0.2,
        "n_fix": 0.0,
        "n_ret": 0.3,
        "p_ret": 0.2,
        "k_ret": 0.3,
        "pest": "TestPest"
    }

    defaults.update(overrides)
    return Crop(**defaults)

@pytest.fixture
def dummy_crops():
    return [
        make_dummy_crop(id=1,name='Σκληρό σιτάρι',family='Poaceae',order='Poales',is_legume=False,root_depth_cm=150,etc_mm=500,sow_month=11,harvest_month=6,t_min=5.0,t_max=32.0,t_opt_min=13.1,t_opt_max=23.9,rain_min_mm=350,rain_max_mm=600,ph_min=5.5,ph_max=8.0,g_min=180,g_max=220,n=13.0,p=2.4,k=3.5, soil_type='loam', residue_fraction=0.3 , n_fix=0.0, n_ret=3.9 ,p_ret=0.72 ,k_ret=1.05, pest='Hessian fly'),
        make_dummy_crop(id=2,name='Κριθάρι',family='Poaceae',order='Poales',is_legume=False,root_depth_cm=120,etc_mm=450,sow_month=11,harvest_month=5,t_min=4.0,t_max=30.0,t_opt_min=11.8,t_opt_max=22.2,rain_min_mm=300,rain_max_mm=500,ph_min=5.5,ph_max=8.0,g_min=120,g_max=160,n=12.0,p=2.0,k=3.0, soil_type='loam', residue_fraction=0.3 , n_fix=0.0, n_ret=3.6 ,p_ret=0.6 ,k_ret=0.9, pest='Bird cherry-oat aphid'),
        make_dummy_crop(id=3,name='Αραβόσιτος',family='Poaceae',order='Poales',is_legume=False,root_depth_cm=200,etc_mm=650,sow_month=4,harvest_month=9,t_min=10.0,t_max=45.0,t_opt_min=20.5,t_opt_max=34.5,rain_min_mm=500,rain_max_mm=800,ph_min=5.5,ph_max=7.8,g_min=110,g_max=150,n=25.0,p=5.0,k=10.0, soil_type='clay loam', residue_fraction=0.3 , n_fix=0.0, n_ret=7.5 ,p_ret=1.5 ,k_ret=3.0, pest='European corn borer'),
        make_dummy_crop(id=4,name='Σόργος',family='Poaceae',order='Poales',is_legume=False,root_depth_cm=200,etc_mm=550,sow_month=5,harvest_month=10,t_min=12.0,t_max=33.0,t_opt_min=15.5,t_opt_max=25.5,rain_min_mm=600,rain_max_mm=1000,ph_min=6.0,ph_max=7.5,g_min=90,g_max=135,n=22.0,p=3.0,k=8.0, soil_type='clay loam', residue_fraction=0.3 , n_fix=0.0, n_ret=6.6 ,p_ret=0.9 ,k_ret=2.4, pest='Sugarcane aphid'),
        make_dummy_crop(id=5,name='Ρύζι',family='Poaceae',order='Poales',is_legume=False,root_depth_cm=50,etc_mm=1000,sow_month=5,harvest_month=9,t_min=15.0,t_max=38.0,t_opt_min=21.9,t_opt_max=31.1,rain_min_mm=800,rain_max_mm=1200,ph_min=5.5,ph_max=7.5,g_min=120,g_max=160,n=20.0,p=4.0,k=5.0, soil_type='loamy clay', residue_fraction=0.3 , n_fix=0.0, n_ret=6.0 ,p_ret=1.2 , k_ret=1.5, pest='Black bean aphid'),
        make_dummy_crop(id=6,name='Βαμβάκι',family='Malvaceae',order='Malvales',is_legume=False,root_depth_cm=200,etc_mm=600,sow_month=4,harvest_month=10,t_min=14.0,t_max=36.0,t_opt_min=18.0,t_opt_max=30.0,rain_min_mm=500,rain_max_mm=900,ph_min=5.5,ph_max=8.0,g_min=150,g_max=200,n=18.0,p=6.0,k=10.0, soil_type='clay loam', residue_fraction=0.2 , n_fix=0.0, n_ret=3.6 ,p_ret=1.2 ,k_ret=2.0, pest='Cotton bollworm'),
        make_dummy_crop(id=7,name='Ηλιοτρόπιο',family='Asteraceae',order='Asterales',is_legume=False,root_depth_cm=200,etc_mm=800,sow_month=3,harvest_month=9,t_min=8.0,t_max=33.0,t_opt_min=15.5,t_opt_max=25.5,rain_min_mm=600,rain_max_mm=1000,ph_min=6.0,ph_max=7.5,g_min=90,g_max=130,n=15.0,p=5.0,k=12.0, soil_type='loamy clay', residue_fraction=0.3 , n_fix=0.0, n_ret=4.5 ,p_ret=1.5 ,k_ret=3.6, pest='Sunflower moth'),
        make_dummy_crop(id=8,name='Ελαιόκαμβη',family='Brassicaceae',order='Brassicales',is_legume=False,root_depth_cm=150,etc_mm=550,sow_month=10,harvest_month=6,t_min=4.0,t_max=30.0,t_opt_min=11.8,t_opt_max=22.2,rain_min_mm=450,rain_max_mm=650,ph_min=5.5,ph_max=8.0,g_min=180,g_max=210,n=25.0,p=5.0,k=10.0, soil_type='clay loam', residue_fraction=0.25 , n_fix=0.0, n_ret=6.25 ,p_ret=1.25 ,k_ret=2.5, pest='Cabbage stem flea beetle'),
        make_dummy_crop(id=9,name='Σουσάμι',family='Pedaliaceae',order='Lamiales',is_legume=False,root_depth_cm=150,etc_mm=500,sow_month=5,harvest_month=9,t_min=15.0,t_max=38.0,t_opt_min=21.9,t_opt_max=31.1,rain_min_mm=400,rain_max_mm=600,ph_min=5.5,ph_max=8.0,g_min=85,g_max=115,n=12.0,p=4.0,k=7.0, soil_type='loam', residue_fraction=0.3 , n_fix=0.0, n_ret=3.6 ,p_ret=1.2 ,k_ret=3.6, pest='Sesame webworm'),
        make_dummy_crop(id=10,name='Κνήκος',family='Asteraceae',order='Asterales',is_legume=False,root_depth_cm=200,etc_mm=500,sow_month=11,harvest_month=6,t_min=5.0,t_max=32.0,t_opt_min=13.1,t_opt_max=23.9,rain_min_mm=400,rain_max_mm=600,ph_min=5.5,ph_max=8.0,g_min=120,g_max=150,n=15.0,p=3.0,k=9.0, soil_type='loam', residue_fraction=0.3 , n_fix=0.0, n_ret=4.5 ,p_ret=1.5 ,k_ret=3.6, pest='Safflower aphid'),
        make_dummy_crop(id=11,name='Σόγια',family='Fabaceae',order='Fabales',is_legume=True,root_depth_cm=150,etc_mm=600,sow_month=5,harvest_month=9,t_min=10.0,t_max=35.0,t_opt_min=17.5,t_opt_max=27.5,rain_min_mm=500,rain_max_mm=700,ph_min=6.0,ph_max=7.5,g_min=110,g_max=150,n=0.0,p=4.0,k=10.0, soil_type='clay loam', residue_fraction=0.3 , n_fix=0.0, n_ret=4.5 ,p_ret=1.5 ,k_ret=3.6, pest='Soybean aphid'),
        make_dummy_crop(id=12,name='Ρεβίθι',family='Fabaceae',order='Fabales',is_legume=True,root_depth_cm=100,etc_mm=425,sow_month=3,harvest_month=7,t_min=4.0,t_max=30.0,t_opt_min=11.8,t_opt_max=22.2,rain_min_mm=300,rain_max_mm=500,ph_min=6.0,ph_max=8.0,g_min=90,g_max=120,n=0.0,p=3.0,k=5.0, soil_type='loam', residue_fraction=0.3 , n_fix=0.0, n_ret=4.5 ,p_ret=1.5 ,k_ret=3.6, pest='Gram pod borer'),
        make_dummy_crop(id=13,name='Φακή',family='Fabaceae',order='Fabales',is_legume=True,root_depth_cm=80,etc_mm=325,sow_month=12,harvest_month=6,t_min=3.0,t_max=28.0,t_opt_min=10.5,t_opt_max=20.5,rain_min_mm=250,rain_max_mm=400,ph_min=6.0,ph_max=8.0,g_min=90,g_max=130,n=0.0,p=2.5,k=4.0, soil_type='loam', residue_fraction=0.3 , n_fix=0.0, n_ret=4.1 ,p_ret=1.5 ,k_ret=3.6, pest='Pea aphid'),
        make_dummy_crop(id=14,name='Κούκι',family='Fabaceae',order='Fabales',is_legume=True,root_depth_cm=120,etc_mm=475,sow_month=11,harvest_month=6,t_min=5.0,t_max=32.0,t_opt_min=13.1,t_opt_max=23.9,rain_min_mm=400,rain_max_mm=600,ph_min=6.0,ph_max=8.0,g_min=150,g_max=180,n=0.0,p=4.0,k=5.0, soil_type='loam', residue_fraction=0.3 , n_fix=0.0, n_ret=5.5 ,p_ret=1.2 ,k_ret=3.6, pest='Black bean aphid'),
        make_dummy_crop(id=15,name='Κτηνοτροφικό μπιζέλι',family='Fabaceae',order='Fabales',is_legume=True,root_depth_cm=100,etc_mm=425,sow_month=11,harvest_month=6,t_min=5.0,t_max=32.0,t_opt_min=13.1,t_opt_max=23.9,rain_min_mm=300,rain_max_mm=500,ph_min=6.0,ph_max=7.5,g_min=90,g_max=120,n=0.0,p=3.0,k=4.0, soil_type='loam', residue_fraction=0.3 , n_fix=0.0, n_ret=2.0 ,p_ret=1.5 ,k_ret=3.6, pest='Pea weevil'),
        make_dummy_crop(id=16,name='Μηδική',family='Fabaceae',order='Fabales',is_legume=True,root_depth_cm=300,etc_mm=900,sow_month=9,harvest_month=6,t_min=2.0,t_max=25.0,t_opt_min=10.0,t_opt_max=20.0,rain_min_mm=500,rain_max_mm=1000,ph_min=6.5,ph_max=8.0,g_min=70,g_max=90,n=0.0,p=5.0,k=15.0, soil_type='loamy clay', residue_fraction=0.3 , n_fix=0.0, n_ret=4.5 ,p_ret=2.5 ,k_ret=3.6, pest='Alfalfa weevil'),
        make_dummy_crop(id=17,name='Πατάτα',family='Solanaceae',order='Solanales',is_legume=False,root_depth_cm=100,etc_mm=600,sow_month=2,harvest_month=6,t_min=5.0,t_max=30.0,t_opt_min=15.0,t_opt_max=25.0,rain_min_mm=350,rain_max_mm=600,ph_min=5.0,ph_max=6.5,g_min=75,g_max=120,n=20.0,p=5.0,k=25.0, soil_type='sandy loam', residue_fraction=0.3 , n_fix=0.0, n_ret=3.5 ,p_ret=1.5 ,k_ret=3.6, pest='Colorado potato beetle'),
        make_dummy_crop(id=18,name='Τομάτα',family='Solanaceae',order='Solanales',is_legume=False,root_depth_cm=120,etc_mm=500,sow_month=3,harvest_month=7,t_min=6.0,t_max=32.0,t_opt_min=18.0,t_opt_max=28.0,rain_min_mm=400,rain_max_mm=700,ph_min=5.0,ph_max=7.0,g_min=90,g_max=120,n=25.0,p=6.0,k=20.0, soil_type='loam', residue_fraction=0.3 , n_fix=0.0, n_ret=2.5 ,p_ret=1.0 ,k_ret=3.2, pest='Tomato leaf miner'),
        make_dummy_crop(id=19,name='Αγγούρι',family='Cucurbitaceae',order='Cucurbitales',is_legume=False,root_depth_cm=90,etc_mm=475,sow_month=4,harvest_month=7,t_min=10.0,t_max=30.0,t_opt_min=20.0,t_opt_max=30.0,rain_min_mm=300,rain_max_mm=600,ph_min=5.5,ph_max=7.5,g_min=50,g_max=70,n=20.0,p=5.0,k=20.0, soil_type='loam', residue_fraction=0.3 , n_fix=3.0, n_ret=4.5 ,p_ret=1.5 ,k_ret=3.6, pest='Cucumber beetle'),
        make_dummy_crop(id=20,name='Καρπούζι',family='Cucurbitaceae',order='Cucurbitales',is_legume=False,root_depth_cm=150,etc_mm=500,sow_month=3,harvest_month=7,t_min=15.0,t_max=35.0,t_opt_min=25.0,t_opt_max=35.0,rain_min_mm=300,rain_max_mm=600,ph_min=5.5,ph_max=7.5,g_min=80,g_max=100,n=15.0,p=4.0,k=15.0, soil_type='loam', residue_fraction=0.3 , n_fix=5.0, n_ret=4.5 ,p_ret=1.5 ,k_ret=1.6, pest='Melon aphid'),
        make_dummy_crop(id=21,name='Πεπόνι',family='Cucurbitaceae',order='Cucurbitales',is_legume=False,root_depth_cm=150,etc_mm=400,sow_month=3,harvest_month=7,t_min=15.0,t_max=33.0,t_opt_min=24.0,t_opt_max=32.0,rain_min_mm=250,rain_max_mm=500,ph_min=5.5,ph_max=7.5,g_min=75,g_max=95,n=15.0,p=4.0,k=13.0, soil_type='loam', residue_fraction=0.3 , n_fix=0.0, n_ret=4.5 ,p_ret=2.5 ,k_ret=1.6, pest='Melon aphid'),
        make_dummy_crop(id=22,name='Πιπερία',family='Solanaceae',order='Solanales',is_legume=False,root_depth_cm=100,etc_mm=550,sow_month=2,harvest_month=8,t_min=10.0,t_max=34.0,t_opt_min=22.0,t_opt_max=30.0,rain_min_mm=300,rain_max_mm=650,ph_min=5.5,ph_max=7.0,g_min=90,g_max=120,n=25.0,p=6.0,k=18.0, soil_type='clay loam', residue_fraction=0.3 , n_fix=0.0, n_ret=4.0 ,p_ret=1.5 ,k_ret=3.4, pest='Pepper weevil'),
        make_dummy_crop(id=23,name='Μελιτζάνα',family='Solanaceae',order='Solanales',is_legume=False,root_depth_cm=120,etc_mm=550,sow_month=2,harvest_month=9,t_min=12.0,t_max=30.0,t_opt_min=20.0,t_opt_max=28.0,rain_min_mm=300,rain_max_mm=700,ph_min=5.5,ph_max=7.5,g_min=100,g_max=140,n=20.0,p=5.0,k=15.0, soil_type='clay loam', residue_fraction=0.3 , n_fix=0.0, n_ret=4.5 ,p_ret=1.5 ,k_ret=2.5, pest='Eggplant fruit and shoot borer'),
        make_dummy_crop(id=24,name='Κρεμμύδι',family='Amaryllidaceae',order='Asparagales',is_legume=False,root_depth_cm=60,etc_mm=450,sow_month=10,harvest_month=6,t_min=5.0,t_max=30.0,t_opt_min=12.0,t_opt_max=22.0,rain_min_mm=300,rain_max_mm=500,ph_min=6.0,ph_max=7.0,g_min=120,g_max=150,n=10.0,p=3.0,k=10.0, soil_type='loam', residue_fraction=0.3 , n_fix=0.0, n_ret=2.5 ,p_ret=1.5 ,k_ret=5.8, pest='Onion thrips'),
        make_dummy_crop(id=25,name='Σκόρδο',family='Amaryllidaceae',order='Asparagales',is_legume=False,root_depth_cm=60,etc_mm=400,sow_month=11,harvest_month=6,t_min=5.0,t_max=32.0,t_opt_min=13.0,t_opt_max=23.0,rain_min_mm=300,rain_max_mm=500,ph_min=6.0,ph_max=7.5,g_min=180,g_max=210,n=8.0,p=2.5,k=8.0, soil_type='loam', residue_fraction=0.3 , n_fix=0.0, n_ret=4.5 ,p_ret=1.5 ,k_ret=3.6, pest='Onion thrips'),
        make_dummy_crop(id=26,name='Καρότο',family='Apiaceae',order='Apiales',is_legume=False,root_depth_cm=60,etc_mm=300,sow_month=3,harvest_month=6,t_min=5.0,t_max=25.0,t_opt_min=15.0,t_opt_max=22.0,rain_min_mm=300,rain_max_mm=400,ph_min=5.5,ph_max=7.0,g_min=70,g_max=120,n=12.0,p=3.0,k=10.0, soil_type='loam', residue_fraction=0.4, n_fix=0.0, n_ret=4.3 ,p_ret=1.5 ,k_ret=3.6, pest='Carrot fly'),
        make_dummy_crop(id=27,name='Μαρούλι',family='Asteraceae',order='Asterales',is_legume=False,root_depth_cm=45,etc_mm=500,sow_month=10,harvest_month=4,t_min=5.0,t_max=25.0,t_opt_min=17.0,t_opt_max=23.0,rain_min_mm=300,rain_max_mm=500,ph_min=6.0,ph_max=7.0,g_min=45,g_max=70,n=10.0,p=3.0,k=10.0, soil_type='loam', residue_fraction=0.4 , n_fix=5.0, n_ret=4.5 ,p_ret=1.5 ,k_ret=3.6, pest='Lettuce aphid'),
        make_dummy_crop(id=28,name='Σπανάκι',family='Amaranthaceae',order='Caryophyllales',is_legume=False,root_depth_cm=45,etc_mm=450,sow_month=9,harvest_month=5,t_min=5.0,t_max=20.0,t_opt_min=15.0,t_opt_max=18.0,rain_min_mm=300,rain_max_mm=400,ph_min=6.0,ph_max=7.5,g_min=45,g_max=60,n=15.0,p=3.0,k=10.0, soil_type='loam', residue_fraction=0.4 , n_fix=0.0, n_ret=4.5 ,p_ret=1.5 ,k_ret=3.6, pest='Vegetable leafminer'),
        make_dummy_crop(id=29,name='Λάχανο',family='Brassicaceae',order='Brassicales',is_legume=False,root_depth_cm=60,etc_mm=350,sow_month=9,harvest_month=5,t_min=5.0,t_max=22.0,t_opt_min=15.0,t_opt_max=20.0,rain_min_mm=250,rain_max_mm=500,ph_min=6.0,ph_max=7.5,g_min=80,g_max=150,n=15.0,p=4.0,k=15.0, soil_type='loam', residue_fraction=0.4 , n_fix=5.0, n_ret=4.5 ,p_ret=1.5 ,k_ret=3.6, pest='Diamondback moth'),
        make_dummy_crop(id=30,name='Μπρόκολο',family='Brassicaceae',order='Brassicales',is_legume=False,root_depth_cm=90,etc_mm=500,sow_month=7,harvest_month=12,t_min=4.0,t_max=25.0,t_opt_min=10.3,t_opt_max=18.7,rain_min_mm=350,rain_max_mm=650,ph_min=6.0,ph_max=7.5,g_min=60,g_max=100,n=15.0,p=4.0,k=15.0, soil_type='loam', residue_fraction=0.4 , n_fix=5.0, n_ret=4.5 ,p_ret=1.5 ,k_ret=3.6, pest='Diamondback moth'),
    ]

# Climate
@pytest.fixture
def dummy_climate():
    return Climate(
        monthly_tmin=[40.0]*12,
        monthly_tmax=[50.0]*12,
        monthly_rain=[0.0]*12,
        monthly_evap=[50.0]*12,
        monthly_rh=[0.6]*12
    )


# Field
@pytest.fixture
def dummy_field(dummy_rotation_info):
    cells = cell_create(dummy_rotation_info)
    field_grid = FieldGrid(cells=cells)
    return Field(
        total_area=12.0,
        grid=field_grid 
    )

@pytest.fixture
def dummy_cell():
    return Cell(
        area=9.0,
        n=10,
        p=5.0,
        k=3.0,
        ph=6.5,
        soil_type="loamy",
        soil_moisture=100.0,
        irrigation=1,
        fertilization=1,
        spraying=1,
        crop_history=[],
        pests=[],
        pest_pressure=0.0,
        crop=None,
        yield_=0.0,
    )

def make_dummy_rotation_info(**overides) -> RotationInfo:
    defaults = {
        "user_id":" ",
        "crops":["Σιτάρι", "Λούπινο"],
        "coordinates":Coordinates(lat=39.0, lng=22.0),
        "area":36.0,
        "soil_type":"loam",
        "irrigation":1,
        "fertilization":1,
        "spraying":1,
        "n":70,
        "p":50,
        "k":60,
        "ph":6.5,
        "machinery":["Θεριζοαλωνιστική"],
        "past_crops":["Βαμβάκι", "Καλαμπόκι"],
        "effective_pairs":[CropPair(crop1="Σιτάρι", crop2="Λούπινο", value=1)],
        "uneffective_pairs":[CropPair(crop1="Βαμβάκι", crop2="Ρύζι", value=-1)],
        "years":3
    }

    defaults.update(overides)
    return RotationInfo(**defaults)



@pytest.fixture
def dummy_rotation_info():
    return RotationInfo(
        user_id="",
        crops=["Σιτάρι", "Λούπινο"],
        coordinates=Coordinates(lat=39.0, lng=22.0),
        area=12.0,
        soil_type="loamy",
        irrigation=1,
        fertilization=1,
        spraying=1,
        n=0,
        p=0,
        k=0,
        ph=4.0,
        machinery=["Θεριζοαλωνιστική"],
        past_crops=["Βαμβάκι", "Καλαμπόκι"],
        effective_pairs=[CropPair(crop1="Σιτάρι", crop2="Λούπινο", value=1)],
        uneffective_pairs=[CropPair(crop1="Βαμβάκι", crop2="Ρύζι", value=-1)],
        years=3
    )



# Pests
def make_dummy_pest_agent(**overrides) -> PestAgent:
    defaults = {
        "name": "Alfalfa weevil",  
        "affected_crops": ["Μηδική"],
        "affected_families": ["Fabaceae"],
        "affected_orders": ["Fabales" ]   
    }
    
    defaults.update(overrides)
    return PestAgent(**defaults)

@pytest.fixture
def dummy_pest_agents():
    return [
        make_dummy_pest_agent(name='Hessian fly', affected_crops=['Σκληρό σιτάρι'], affected_families=['Poaceae'], affected_orders=['Poales']),
        make_dummy_pest_agent(name='Bird cherry-oat aphid', affected_crops=['Κριθάρι'], affected_families=['Poaceae'], affected_orders=['Poales']),
        make_dummy_pest_agent(name='Eggplant fruit and shoot borer', affected_crops=['Αραβόσιτος', 'Μελιτζάνα'], affected_families=['Poaceae', 'Solanaceae'], affected_orders=['Poales', 'Solanales']),
        make_dummy_pest_agent(name='Sugarcane aphid', affected_crops=['Σόργος'], affected_families=['Poaceae'], affected_orders=['Poales']),
        make_dummy_pest_agent(name='Brown planthopper', affected_crops=['Ρύζι'], affected_families=['Poaceae'], affected_orders=['Poales']),
        make_dummy_pest_agent(name='Cotton bollworm', affected_crops=['Βαμβάκι'], affected_families=['Malvaceae'], affected_orders=['Malvales']),
        make_dummy_pest_agent(name='Sunflower moth', affected_crops=['Ηλιοτρόπιο'], affected_families=['Asteraceae'], affected_orders=['Asterales']),
        make_dummy_pest_agent(name='Cabbage stem flea beetle', affected_crops=['Ελαιόκαμβη'], affected_families=['Brassicaceae'], affected_orders=['Brassicales']),
        make_dummy_pest_agent(name='Sesame webworm', affected_crops=['Σουσάμι'], affected_families=['Pedaliaceae'], affected_orders=['Lamiales']),
        make_dummy_pest_agent(name='Safflower aphid', affected_crops=['Κνήκος'], affected_families=['Asteraceae'], affected_orders=['Asterales']),
        make_dummy_pest_agent(name='Soybean aphid', affected_crops=['Σόγια'], affected_families=['Asteraceae'], affected_orders=['Asterales']),
        make_dummy_pest_agent(name='Gram pod borer', affected_crops=['Ρεβίθι'], affected_families=['Fabaceae'], affected_orders=['Fabales']),
        make_dummy_pest_agent(name='Pea aphid', affected_crops=['Φακή'], affected_families=['Fabaceae'], affected_orders=['Fabales']),
        make_dummy_pest_agent(name='Black bean aphid', affected_crops=['Κούκι'], affected_families=['Fabaceae'], affected_orders=['Fabales']),
        make_dummy_pest_agent(name='Pea weevil', affected_crops=['Κτηνοτροφικό μπιζέλι'], affected_families=['Fabaceae'], affected_orders=['Fabales']),
        make_dummy_pest_agent(name='Alfalfa weevil', affected_crops=['Μηδική'], affected_families=['Fabaceae'], affected_orders=['Fabales']),
        make_dummy_pest_agent(name='Colorado potato beetle', affected_crops=['Πατάτα'], affected_families=['Solanaceae'], affected_orders=['Solanales']),
        make_dummy_pest_agent(name='Tomato leaf miner', affected_crops=['Τομάτα'], affected_families=['Solanaceae'], affected_orders=['Solanales']),
        make_dummy_pest_agent(name='Cucumber beetle', affected_crops=['Αγγούρι'], affected_families=['Cucurbitaceae'], affected_orders=['Cucurbitales']),
        make_dummy_pest_agent(name='Melon aphid', affected_crops=['Καρπούζι', 'Πεπόνι'], affected_families=['Cucurbitaceae'], affected_orders=['Cucurbitales']),
        make_dummy_pest_agent(name='Pepper weevil', affected_crops=['Πιπερία'], affected_families=['Solanaceae'], affected_orders=['Solanales']),
        make_dummy_pest_agent(name='Onion thrips', affected_crops=['Κρεμμύδι', 'Σκόρδο'], affected_families=['Amaryllidaceae'], affected_orders=['Asparagales']),
        make_dummy_pest_agent(name='Carrot fly', affected_crops=['Καρότο'], affected_families=['Apiaceae'], affected_orders=['Apiales']),
        make_dummy_pest_agent(name='Lettuce aphid', affected_crops=['Μαρούλι'], affected_families=['Asteraceae'], affected_orders=['Asterales']),
        make_dummy_pest_agent(name='Vegetable leafminer', affected_crops=['Σπανάκι'], affected_families=['Amaranthaceae'], affected_orders=['Caryophyllales']),
        make_dummy_pest_agent(name='Diamondback moth', affected_crops=['Λάχανο', 'Μπρόκολο'], affected_families=['Brassicaceae'], affected_orders=['Brassicales']),
    ]

@pytest.fixture
def dummy_past_pest_agents():
    return [
        make_dummy_pest_agent(name='Bird cherry-oat aphid', affected_crops=['Κριθάρι'], affected_families=['Poaceae'], affected_orders=['Poales']),
        make_dummy_pest_agent(name='Sugarcane aphid', affected_crops=['Σόργος'], affected_families=['Poaceae'], affected_orders=['Poales']),
    ]

@pytest.fixture
def dummy_pest_manager(dummy_pest_agents, dummy_past_pest_agents):
    return PestSimulationManager(
        pest_agents=dummy_pest_agents, 
        past_pest_agents=dummy_past_pest_agents,   
    )


# Years
@pytest.fixture
def dummy_years():
    return 7

# Past crops
@pytest.fixture
def dummy_past_crops():
    return ["Κριθάρι", "Σόργος"]

# Missing machinery
@pytest.fixture
def dummy_missing_machinery():
    return  ["Σπαρτική", "Θεριζοαλωνιστική"]

# Required machinery
@pytest.fixture
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

@pytest.fixture
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


# Farmer knowlegde
@pytest.fixture
def dummy_farmer_knowledge():
    effective = [
        CropPair(crop1="Σιτάρι", crop2="Λούπινο", value=1),
        CropPair(crop1="Ρύζι", crop2="Φασόλια", value=1),
    ]

    uneffective = [
        CropPair(crop1="Καλαμπόκι", crop2="Πατάτα", value=-1),
        CropPair(crop1="Κριθάρι", crop2="Σιτάρι", value=-1),
    ]

    past = ["Σιτάρι", "Καλαμπόκι", "Ρύζι"]

    return FarmerKnowledge(
        effective_pairs=effective,
        uneffective_pairs=uneffective,
        past_crops=past
    )

# Beneficial roations
@pytest.fixture
def dummy_beneficial_rotations():
    return [
        ["Σιτάρι", "Λούπινο"],               
        ["Καλαμπόκι", "Φασόλια", "Μηδική"],  
        ["Ρύζι", "Φασόλια"],                
    ]

"""
----------------------------------
     RANDOM VALUES TO TEST GA
----------------------------------
"""
crops = [
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
    "Πιπερία",
    "Μελιτζάνα",
    "Κρεμμύδι",
    "Σκόρδο",
    "Καρότο",
    "Μαρούλι", 
    "Σπανάκι", 
    "Λάχανο", 
    "Μπρόκολο"
]
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


@pytest.mark.fixture
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

@pytest.fixture
def random_dummy_field(random_dummy_rotation_info):
    cells = cell_create(random_dummy_rotation_info)
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
        fertilization=([0, 1, 2, 3]),
        spraying=([0, 1, 2, 3]),
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

@pytest.fixture
def random_dummy_years():
    return random.randint(3, 10)

@pytest.fixture
def random_dummy_farmer_knowledge():
    eff_len = random.randint(1, 4)
    unEff_len = random.randint(1,4)

    effective_pairs = []
    uneffctive_pairs = []

    for _ in range(eff_len):
        crop1 = random.choice(crops)
        crop2 = random.choice(crops)
        value = random.randint(1,3)

        while crop1 == crop2:
            crop2 = random.choice(crops)
        
        pair = CropPair(crop1=crop1, crop2=crop2, value=value)
        effective_pairs.append(pair)

    for _ in range(unEff_len):
        crop1 = random.choice(crops)
        crop2 = random.choice(crops)
        value = random.randint(1,3)

        while crop1 == crop2:
            crop2 = random.choice(crops)
        
        pair = CropPair(crop1=crop1, crop2=crop2, value=value)
        uneffctive_pairs.append(pair)
    
    return FarmerKnowledge(
        effective_pairs=effective_pairs,
        uneffective_pairs=uneffctive_pairs,
        past_crops=[]
    )
    

@pytest.fixture
def random_dummy_beneficial_rotations():
    num_rotations = random.randint(1, 5)
    beneficial_rotations = []
    for _ in range(num_rotations):
        rotation_len = random.randint(2, 5)
        rotation = []
        for _ in range(rotation_len):
            crop = random.choice(crops)
            rotation.append(crop)
        
        beneficial_rotations.append(rotation)


    return beneficial_rotations

@pytest.fixture
def random_dummy_missing_machinery():
    num_missing = random.randint(1,4)
    missing_machinery = []

    for _ in range(num_missing):
        machinery = random.choice(unique_machinery)
        while machinery in missing_machinery:
            machinery = random.choice(unique_machinery)
        missing_machinery.append(machinery)

    return missing_machinery

@pytest.fixture
def random_dummy_past_crops():
    crop1 = random.choice(crops)
    crop2 = random.choice(crops)
    return [crop1, crop2]
