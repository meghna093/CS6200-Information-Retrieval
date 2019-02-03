import java.io.File;
import java.io.FileReader;
import java.io.IOException;
import java.util.ArrayList;
import java.io.FileWriter;
import org.apache.lucene.analysis.Analyzer;
import org.apache.lucene.analysis.core.SimpleAnalyzer;
import org.apache.lucene.document.Document;
import org.apache.lucene.document.Field;
import org.apache.lucene.document.StringField;
import org.apache.lucene.document.TextField;
import org.apache.lucene.index.DirectoryReader;
import org.apache.lucene.index.IndexReader;
import org.apache.lucene.index.IndexWriter;
import org.apache.lucene.index.IndexWriterConfig;
import org.apache.lucene.queryparser.classic.QueryParser;
import org.apache.lucene.search.IndexSearcher;
import org.apache.lucene.search.Query;
import org.apache.lucene.search.ScoreDoc;
import org.apache.lucene.search.TopScoreDocCollector;
import org.apache.lucene.store.FSDirectory;
import org.apache.lucene.util.Version;

/**
 * To create Apache Lucene index in a folder and add files into this index based
 * on the input of the user.
 */

/**
 * @author Sachin Haldavanekar
 * This program assumes that if the index folder is present then it should only 
 * perform a query operation else it should first index all files in source 
 * folder and then store indexes in index folder.
 * 
 * To completely index all files again, delete the index folder and run the 
 * program.
 * 
 */
public class Lucene{

	// Declaring Constants
	private static final String SYS_USER_DIR = System.getProperty("user.dir") ;
	private static final String OUTPUT_FILE_NAME = "Lucene_Result.txt";
	private static final int MAX_RESULTS_PER_QUERY = 100;

	// Declaring static variables
	private static Analyzer analyzer = new SimpleAnalyzer(Version.LUCENE_47);
	private IndexWriter writer;
	private ArrayList<File> queue = new ArrayList<File>();


	/** Main function
	 *  
	 * @param args
	 * 			args[0] - will contain path of the folder to store index in.
	 * 			args[1] - will contain path of the folder to get raw documents from.
	 *			All queries will be in the args and each word in a query will be
	 * 			delimited by space
	 * 
	 * @throws IOException
	 * 			when exception occurs.
	 * **/
	public static void main(String[] args) throws IOException {

		// Chooses default index location if the args[0] is an empty string.
		String indexLocation = args[0].equalsIgnoreCase("")? SYS_USER_DIR + "/index":args[0];
		//==========================================================
		// Index files if not already indexed
		//==========================================================
		indexer(args[1],indexLocation);
		// =========================================================
		// Now search
		// =========================================================
		findResultsAndPrint(args, indexLocation);
	}

	/**
	 * finds Result for all Queries and calls the printToFile function.
	 * 
	 * @param rawFileLoc
	 * 			denotes the path where the raw source code files are located.
	 * 		  indexLocation
	 * 			denotes the path where indexes have to be stored.
	 * 				
	 * @throws java.io.IOException
	 *             	when exception closing
	 */
	private static void indexer(String rawFileLoc, String indexLocation) {

		File f = new File(indexLocation); 
		Lucene indexer = null;

		if (!f.exists()) {
			if (f.mkdir()) {
				try {
					indexer = new Lucene(f);
					rawFileLoc = rawFileLoc.equalsIgnoreCase("")? SYS_USER_DIR + "/source":rawFileLoc;
					indexer.indexFileOrDirectory(rawFileLoc);	// try to add file into the index
					// ===================================================
					// after adding, we always have to call the
					// closeIndex, otherwise the index is not created
					// ===================================================
					indexer.closeIndex();
				} catch (Exception e) {
					System.out.println("Error indexing File/Directory" + rawFileLoc + " : "
							+ e.getMessage());
					System.exit(-1);
				}
			}
		}
	}



	/**
	 * finds Result for all Queries and calls the printToFile function.
	 * 
	 * @param queries
	 * 				stores the args array.
	 * 		  indexLocation
	 * 				denotes the path where indexes are stored.
	 * 
	 * @throws java.io.IOException
	 *          when exception closing
	 */
	private static void findResultsAndPrint(String[] queries, String indexLocation) throws IOException {
		IndexReader reader = DirectoryReader.open(FSDirectory.open(new File(indexLocation)));
		IndexSearcher searcher = new IndexSearcher(reader);
		TopScoreDocCollector collector = null;		
		FileWriter docFileWriter = new FileWriter(new File(OUTPUT_FILE_NAME));

		for(int i = 2; i < queries.length; i++)	{
			try {
				String input_query = queries[i].split(":")[1];
				Query q = new QueryParser(Version.LUCENE_47, "contents", analyzer)
						.parse(input_query.toLowerCase());
				collector = TopScoreDocCollector.create(3204, true);
				searcher.search(q, collector);
				ScoreDoc[] hits = collector.topDocs().scoreDocs;

				//====================================
				// Display Results to console and File
				//====================================				
				printToFile(hits, searcher, queries[i].split(":")[0], docFileWriter);
			}
			catch(Exception e){
				System.out.println("Error in Querying" + e.getMessage());
				System.exit(-1);
			}
		}
		docFileWriter.close();
	}

	/**
	 * Prints results to a file
	 * 
	 * @param : hits
	 * 				stores all the htis found for a particular query.
	 * 			searcher
	 * 				IndexSearcher of Lucene to find a doc by its docId.
	 * 			docFileWriter
	 * 				FileWriter object to write output to text file.
	 * 
	 * @throws java.io.IOException
	 *             when exception closing
	 */
	private static void printToFile(ScoreDoc[] hits, IndexSearcher searcher, String Qid, FileWriter docFileWriter) throws IOException {
		try {			
			//System.out.println("Found " + hits.length + " hits.");	//SOP
			for (int j = 0; j < Math.min(MAX_RESULTS_PER_QUERY, hits.length); ++j) {
				int docId = hits[j].doc;
				Document d = searcher.doc(docId);
				String filename = d.get("filename");
				filename = filename.substring(0, filename.length() - 5);
				String concatenatedOutput = 
						Qid + 
						" Q0" + 
						" " +  filename +
						"\t" + (j + 1) +  
						"\t" + hits[j].score + 
						"\tLucene" +
						System.lineSeparator();
				System.out.print(concatenatedOutput);				//SOP
				docFileWriter.write(concatenatedOutput);
			}
			docFileWriter.write("\n\n");
		}
		catch(Exception e){
			System.out.println("Error in Printing to file" + e.getMessage());
			System.exit(-1);
		}
	}

	/**
	 * Constructor
	 * 
	 * @param indexDir
	 *            the name of the folder in which the index should be created
	 * @throws java.io.IOException
	 *             when exception creating index.
	 */
	Lucene(File f) throws IOException {

		FSDirectory dir = FSDirectory.open(f);

		IndexWriterConfig config = new IndexWriterConfig(Version.LUCENE_47,
				analyzer);

		writer = new IndexWriter(dir, config);
	}

	/**
	 * Indexes a file or directory
	 * 
	 * @param fileName
	 *            the name of a text file or a folder we wish to add to the
	 *            index
	 * @throws java.io.IOException
	 *             when exception
	 */
	public void indexFileOrDirectory(String fileName) throws IOException {
		// ===================================================
		// gets the list of files in a folder (if user has submitted
		// the name of a folder) or gets a single file name (is user
		// has submitted only the file name)
		// ===================================================
		addFiles(new File(fileName));

		int originalNumDocs = writer.numDocs();
		for (File f : queue) {
			FileReader fr = null;
			try {
				Document doc = new Document();
				// ===================================================
				// add contents of file
				// ===================================================
				fr = new FileReader(f);
				doc.add(new TextField("contents", fr));
				doc.add(new StringField("path", f.getPath(), Field.Store.YES));
				doc.add(new StringField("filename", f.getName(),Field.Store.YES));

				writer.addDocument(doc);
				System.out.println("Added: " + f);			//SOP
			} catch (Exception e) {
				System.out.println("Could not add: " + f);
			} finally {
				fr.close();
			}
		}

		int newNumDocs = writer.numDocs();
		System.out.println("");										//SOP
		System.out.println("************************");				//SOP
		System.out.println((newNumDocs - originalNumDocs) + " documents added.");		//SOP
		System.out.println("************************");				//SOP

		queue.clear();
	}

	/**
	 * Add files for indexing
	 * 
	 * @param file
	 * 			File to be added.
	 * 
	 */
	private void addFiles(File file) { 
		if (!file.exists()) {
			System.out.println(file + " does not exist.");
		}
		if (file.isDirectory()) {
			for (File f : file.listFiles()) {
				addFiles(f);
			}
		} else {
			String filename = file.getName().toLowerCase();
			// ===================================================
			// Only index text files
			// ===================================================
			if (filename.endsWith(".htm") || filename.endsWith(".html")
					|| filename.endsWith(".xml") || filename.endsWith(".txt")) {
				queue.add(file);
			} else {
				System.out.println("Skipped " + filename);
			}
		}
	}

	/**
	 * Close the index.
	 * 
	 * @throws java.io.IOException
	 *             when exception closing
	 */
	public void closeIndex() throws IOException {
		writer.close();
	}
}
