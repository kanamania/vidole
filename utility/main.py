from concurrent import futures
from flask import Flask
from proto.db_pb2_grpc import add_DBServicer_to_server, DBServicer
from utility.proto.fs_pb2_grpc import FSServicer, add_FSServicer_to_server
from utility.proto.mail_pb2_grpc import MAILServicer, add_MAILServicer_to_server
import grpc
from implementation.db import db
from implementation.fs import fs
from implementation.mail import mail
app = Flask(__name__)


@app.route("/")
def index():
    return "<p>Hello, World!, from utility service</p>"


class DB(DBServicer):

    def PerformBackup(self, request, context):
        super().PerformBackup(request, context)
        db.backup(request, context)

    def PerformRestore(self, request, context):
        super().PerformRestore(request, context)
        db.restore(request, context)

    def PerformReplication(self, request, context):
        super().PerformReplication(request, context)
        db.replicate(request, context)


class FS(FSServicer):

    def RemoveCache(self, request, context):
        super().RemoveCache(request, context)
        fs.removeCache(request, context)

    def ResizeImage(self, request, context):
        super().ResizeImage(request, context)
        fs.resizeImage(request, context)

    def CompressImage(self, request, context):
        super().CompressImage(request, context)
        fs.compressImage(request, context)

    def CompressArchive(self, request, context):
        super().CompressArchive(request, context)
        fs.compressArchive(request, context)


class MAIL(MAILServicer):

    def SendMail(self, request, context):
        super().SendMail(request, context)
        mail.sendMail(request, context)

    def SendCampaign(self, request, context):
        super().SendCampaign(request, context)
        mail.sendCampaign(request, context)


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
