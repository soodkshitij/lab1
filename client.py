'''
################################## client.py #############################
# 
################################## client.py #############################
'''
import grpc
import datastore_pb2
import argparse
import sys

PORT=3000
HOST = None

check_input = lambda op : op in ['put','get']

class DatastoreClient():
    
    def __init__(self, host='0.0.0.0', port=PORT):
        self.channel = grpc.insecure_channel('%s:%d' % (host, port))
        self.stub = datastore_pb2.DatastoreStub(self.channel)

    def put(self, value):
        return self.stub.put(datastore_pb2.Request(data=value)).data

    def get(self, key):
        return (self.stub.get(datastore_pb2.Request(data=key))).data
    
def fetch_inputs():
    client = DatastoreClient(host=HOST)
    while True:
        try:
            method = input("Enter the operation you want to perform.PUT or GET\n").lower()
            if not check_input(method):
                print("\nIllegal operation\n")
                continue
            
            if method == "put":
                val = input("\nEnter the value you want to store.\n").strip()
                if not val:
                    print("\nIllegal value\n")
                    continue
                d_key = client.put(val)
                print("\nKey for value {} is {}\n".format(val, d_key))
                
                
            else:
                key = input("\nEnter the key you want to retrieve.\n").strip()
                if not key:
                    print("\nIllegal key\n")
                    continue
                d_val = client.get(key)
                if not d_val:
                    print("\nNo value found for give key {}".format(key))
                    continue
                print("\nValue for key {} is {}\n".format(key,d_val))
                
                
        except KeyboardInterrupt:
            print("Terminating program......")
            sys.exit(1)

def main():
    global HOST
    parser = argparse.ArgumentParser()
    parser.add_argument("host", help="host where grpc server is running")
    args = parser.parse_args()
    HOST = args.host
    fetch_inputs()
    


if __name__ == "__main__":
    main()

