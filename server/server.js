var cluster = require('cluster');
var numCPUs = require('os').cpus().length;

var Thrift = require('thrift');
var PropertyService = require('../gen-nodejs/PropertyService');
var ttypes = require('../gen-nodejs/juwai_types');

var Sequelize = require('sequelize')
var sequelize = new Sequelize('mysql://localhost/db', {
	logging: false,
	pool: { maxConnections: 50, maxIdleTime: 30 }
});

var Property = sequelize.define('Property', {
	id:		Sequelize.BIGINT,
	description:	Sequelize.TEXT
},{
	timestamps: false,
	tableName: 'property'
});

if (cluster.isMaster) {
	for (var i = 0; i < numCPUs; i++) {
		cluster.fork();
	}
	cluster.on('exit', function(worker, code, signal) {
		console.log('worker ' + worker.process.pid + ' died');
	});
} else {
	var server = Thrift.createServer(PropertyService, {
		getProperty: function(id, result) {
			//sequelize.query('select sleep(1)')
			Property.find(parseInt(id))
			.success(function(prop) {
				if(null === prop) {
					result(new NoSuchObject({message: 'No property with id ' + id}));
				} else {
					result(null, new TProperty(prop));
				}
			})
			.error(function(err) {
				result(new SelectFailed({message: 'Could not select property'}));
			});
		},
		addProperty: function(tProp, result) {
			Property.build(tProp)
			.save()
			.success(function(prop) {
				result(null);
			})
			.error(function(err) {
				result(new InsertFailed({message: 'Could not save property'}));
			});
		}
	},{ transport: Thrift.TFramedTransport });

	console.log('Starting server...');
	server.listen(9090);
}
