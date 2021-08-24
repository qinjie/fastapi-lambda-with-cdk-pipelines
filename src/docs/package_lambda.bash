# Create/activate virtual environment and install dependencies
python -m venv venv
source ./venv/bin/activate
pip install -r requirements.txt

# Zip source files
root_dir=$PWD
venv_dir="$root_dir/venv/lib/python3.8/site-packages"
app_dir="$root_dir/app"

ls -ld $root_dir
ls -ld $venv_dir
ls -ld $app_dir

cd $root_dir && rm -f lambda.zip
cd $venv_dir && zip -r9 "$root_dir/lambda.zip" .
cd $root_dir && zip -g lambda.zip -r app

