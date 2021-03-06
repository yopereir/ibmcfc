/*
 * SPDX-License-Identifier: Apache-2.0
 */

'use strict';

const { Contract } = require('fabric-contract-api');

class MyAssetContract extends Contract {

  // Gets abid criteria info
  async doesAuctionExist (ctx, auctionID){
    const buffer = await ctx.stub.getState(auctionID);
    return (!!buffer && buffer.length > 0);
  }

  // Gets abid criteria info
  async getAuctionInfo (ctx, auctionID){
    const exists = await this.doesAuctionExist(ctx, auctionID);
    if (!exists) {
      throw new Error('The asset '+auctionID+' does not exist');
    }
    const buffer = await ctx.stub.getState(auctionID);
    const auction = JSON.parse(buffer.toString());
    const result = { bids: auction.bids, endDate: auction.endDate, origin: auction.origin, destination: auction.destination };
    return result;
  }

  // Edit auction end date
  async editAuctionEndDate (ctx, reliefCenterID, daysToEnd = 7){
    const exists = await this.doesAuctionExist(ctx, reliefCenterID);
    if (!exists) {
      throw new Error(`The asset ${reliefCenterID} doesn't exists`);
    }
    const buffer = await ctx.stub.getState(reliefCenterID);
    const auctionInfo = JSON.parse(buffer.toString());
    auctionInfo.endDate = auctionInfo.startDate + parseInt(daysToEnd)*3600000*24;
    await ctx.stub.putState(reliefCenterID, Buffer.from(JSON.stringify(auctionInfo)));
    console.info('Auction end date edited.');
  }

  // Creates auction given auction info and resourCenterID
  async initiateAuction (ctx, reliefCenterID, origin, destination, daysToEnd = 7){
    const exists = await this.doesAuctionExist(ctx, reliefCenterID);
    if (exists) {
      throw new Error(`The asset ${reliefCenterID} already exists`);
    }
    const bids =[];
    const auctionInfo={
      origin,
      destination,
      bids: bids,
      startDate: Date.now(),
      endDate: parseInt(daysToEnd)*3600000*24+Date.now(),
    };
    const auctionID = reliefCenterID;
    await ctx.stub.putState(auctionID, Buffer.from(JSON.stringify(auctionInfo)));
    console.info('Auction created');
  }

  // Allows a transportation company to bid
  async bid (ctx, auctionID, costOfHire, driverName, truckNumber){
    const exists = await this.doesAuctionExist(ctx, auctionID);
    if (!exists) throw new Error('The auction '+auctionID+' does not exist');
    const buffer = await ctx.stub.getState(auctionID);
    const auctionInfo = JSON.parse(buffer.toString());
    if (Date.now() > auctionInfo.endDate) throw new Error('The auction '+auctionID+' has closed');
    const bid={};
    bid.CostOfHire=costOfHire;
    bid.DriverName=driverName;
    bid.TruckNumber=truckNumber;
    auctionInfo.bids.push(bid);
    await ctx.stub.putState(auctionID, Buffer.from(JSON.stringify(auctionInfo)));
    console.info('Created bid');
  }

  async getLowestBid (ctx, auctionID){
    const exists = await this.doesAuctionExist(ctx, auctionID);
    if (!exists) {
      throw new Error('The asset '+auctionID+' does not exist');
    }
    const buffer = await ctx.stub.getState(auctionID);
    const auction = JSON.parse(buffer.toString());
    let lowestBid =auction.bids[0];
    auction.bids.forEach((bid)=>{if(bid.CostOfHire>lowestBid.CostOfHire)lowestBid=bid;});
    return lowestBid;
  }

  //Cloest auction after a specified time, selecting the lowest bid
  async closeAuction (ctx, reliefCenterID){
    const exists = await this.doesAuctionExist(ctx, reliefCenterID);
    if (!exists) {
      throw new Error(`The asset ${reliefCenterID} does not exist`);
    }
    await ctx.stub.deleteState(reliefCenterID);
  }

}

module.exports = MyAssetContract;
