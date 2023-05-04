for i in {0..1..1}
do
    echo "Downloading files for node 00$i"
    aws s3 cp s3://nrel-pds-porotomo/Nodal/nodal_sac/00$i D:/Brady_Nodal/00$i --recursive --exclude "*" --include "20160309*.sac" --no-sign-request
done