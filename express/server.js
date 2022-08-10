// Imports
const express = require("express");
const graphql = require("graphql");
const { graphqlHTTP } = require("express-graphql");
const mongoose = require("mongoose");
const bodyParser = require("body-parser");
const cors = require("cors");
require("dotenv/config");

// Import api-version we're currently using
const apiv1 = require("./routes/v1/index");

// Global Variables
const app = express();
const PORT = 3001;

// Mongoose connection - Connect To DB
mongoose.connect(
  (uri = process.env.DB_CONNECTION),
  (callback = () => console.log("Connected to mongodb - mongoose"))
);

// Enable Cors
app.use(cors());

// Use bodyParser
app.use(bodyParser.json());

// Using api version=1
app.use("/api/v1", apiv1);

app.listen(3001);

// const UserType = new graphql.GraphQLObjectType({
//   name: "User",
//   fields: () => ({
//     id: { type: graphql.GraphQLInt },
//     name: { type: graphql.GraphQLString },
//   }),
// });

// const RootQuery = new graphql.GraphQLObjectType({
//   name: "RootQueryType",
//   fields: {},
// });
// const Mutation = "mutation";

// const schema = new graphql.GraphQLSchema({
//   query: RootQuery,
//   mutation: Mutation,
// });

// app.use(
//   "/graphql",
//   graphqlHTTP({
//     schema,
//     graphiql: true,
//   })
// );
