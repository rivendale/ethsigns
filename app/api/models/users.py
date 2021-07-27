
from app import db
from .base import ModelOperations


association_table = db.Table('user_sign_hashes', db.Model.metadata,
                             db.Column('user_id', db.Integer,
                                       db.ForeignKey('metamask_user.id')),
                             db.Column('sign_hash', db.Integer,
                                       db.ForeignKey('sign_hash.id'))
                             )
dob_association_table = db.Table('user_transactions', db.Model.metadata,
                                 db.Column('user_id', db.Integer,
                                           db.ForeignKey('metamask_user.id')),
                                 db.Column('mint_sign', db.Integer,
                                           db.ForeignKey('mint_sign.id'))
                                 )
nft_association_table = db.Table('user_nfts', db.Model.metadata,
                                 db.Column('user_id', db.Integer,
                                           db.ForeignKey('metamask_user.id')),
                                 db.Column('user_nft', db.Integer,
                                           db.ForeignKey('NFT.id'))
                                 )


class SignHash(db.Model, ModelOperations):
    id = db.Column(db.Integer, primary_key=True)
    signhash = db.Column(db.String(500), index=True, unique=True)

    def __repr__(self):
        return '<SignHash {}>'.format(self.id)

    def __init__(self, signhash):
        """Constructor object
        Args:
            signhash (dict): signhash data to be saved in DB
        Returns:
            None"""
        self.signhash = signhash.get('sign_hash')


class MetamaskUser(db.Model, ModelOperations):
    id = db.Column(db.Integer, primary_key=True)
    address = db.Column(db.String(120), index=True, unique=True)
    sign_hashes = db.relationship("SignHash",
                                  secondary=association_table)

    mint_sign = db.relationship("MintSign",
                                secondary=dob_association_table)
    user_nfts = db.relationship("NFT",
                                secondary=nft_association_table)

    @property
    def tokens_minted(self):
        """
        Get total tokens minted
        """
        return len([sign for sign in self.mint_sign if sign.minted])

    @property
    def pending_mints(self):
        """
        Get total tokens pending mints
        """
        return len([sign for sign in self.mint_sign if not sign.minted])

    def __repr__(self):
        return '<User {}>'.format(self.address)

    def __init__(self, user):
        """Constructor object
        Args:
            user (dict): user data to be saved in DB
        Returns:
            None"""
        self.address = user.get('address')


class MintSign(db.Model, ModelOperations):
    id = db.Column(db.Integer, primary_key=True)
    dob = db.Column(db.Date, index=True, unique=False)
    created_at = db.Column(db.DateTime, index=True, unique=False)
    transaction_hash = db.Column(db.String(500), index=True)
    mint_hash = db.Column(db.String(500), index=True, unique=False)
    minted = db.Column(db.Boolean, index=True, default=False)

    def __repr__(self):
        return '<MintSign {}>'.format(self.id)

    def __init__(self, data):
        """Constructor object
        Args:
            data (dict): data to be saved in DB
        Returns:
            None"""
        self.dob = data.get('dob')
        self.transaction_hash = data.get('transaction_hash')
        self.created_at = data.get('created_at')

    @property
    def user_address(self):
        user = MetamaskUser.query.filter(
            MetamaskUser.mint_sign.any(id=self.id)).first()
        return user.address
