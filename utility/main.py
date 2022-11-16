from concurrent import futures
from flask import Flask
from proto.db_pb2_grpc import add_DBServicer_to_server, DBServicer
from utility.proto.fs_pb2_grpc import FSServicer, add_FSServicer_to_server
from utility.proto.mail_pb2_grpc import MAILServicer, add_MAILServicer_to_server
import grpc

app = Flask(__name__)


@app.route("/")
def index():
    return "<p>Hello, World!, from utility service</p>"


class DB(DBServicer):

    def PerformBackup(self, request, context):
        return super().PerformBackup(request, context)

    def PerformRestore(self, request, context):
        return super().PerformRestore(request, context)

    def PerformReplication(self, request, context):
        return super().PerformReplication(request, context)


class FS(FSServicer):

    def RemoveCache(self, request, context):
        return super().RemoveCache(request, context)

    def ResizeImage(self, request, context):
        return super().ResizeImage(request, context)

    def CompressImage(self, request, context):
        return super().CompressImage(request, context)

    def CompressArchive(self, request, context):
        return super().CompressArchive(request, context)


class MAIL(MAILServicer):

    def SendMail(self, request, context):
        return super().SendMail(request, context)

    def SendCampaign(self, request, context):
        return super().SendCampaign(request, context)


def server():
    engine = grpc.server(futures.ThreadPoolExecutor(max_workers=4))
    add_DBServicer_to_server(DB(), engine)
    add_FSServicer_to_server(FS(), engine)
    add_MAILServicer_to_server(MAIL(), engine)
    engine.add_insecure_port('[::]:50051')
    print("gRPC starting")
    engine.start()
    engine.wait_for_termination()


server()
