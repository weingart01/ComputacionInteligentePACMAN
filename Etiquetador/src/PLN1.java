/*
 * To change this license header, choose License Headers in Project Properties.
 * To change this template file, choose Tools | Templates
 * and open the template in the editor.
 */

/**
 * @author weingart, joaquim
 */
import java.io.BufferedReader;
import java.io.BufferedWriter;
import java.io.File;
import java.io.FileInputStream;
import java.io.FileNotFoundException;
import java.io.FileOutputStream;
import java.io.FileReader;
import java.io.IOException;
import java.io.InputStreamReader;
import java.io.OutputStreamWriter;
import java.io.UnsupportedEncodingException;
import java.util.HashMap;
import java.util.Iterator;
import java.util.Map;
import java.util.logging.Level;
import java.util.logging.Logger;

public class PLN1 {

    public static void main(String[] args) throws FileNotFoundException, UnsupportedEncodingException, IOException {
        // Pasamos como argumento 0 el corpus a entrenar
        args[0] = "corpus.txt";
        Training(args[0]);
        // Una vez tenemos el modelo etiquetamos el fichero del argumento 1
        // en otro fichero
        args[1] = "test_1.txt";
        Tagging(args[1]);
        // Comparamos el nuevo fichero etiquetado con el corpus entrenado con el fichero correctamente etiquetado
        args[2] = "gold_standard_1.txt";
        Avaluation(args[1].replace(".txt","tagged.txt"), args[2]);
    }


    static void Training(String path) throws UnsupportedEncodingException, FileNotFoundException {
        HashMap< String, HashMap< String, Integer>> corpus = new HashMap<String, HashMap<String, Integer>>();
        String line = "", word, tag;
        int times;
        BufferedReader file = new BufferedReader(new InputStreamReader(new FileInputStream(path), "ISO-8859-1"));
        try {
            // Comprobamos linea a linea hasta que el final del archivo
            while ((line = file.readLine()) != null) {
            	// Extraemos para cada linea la palabra y su tag asignado
                String[] tokens = line.split("\t");
                word = tokens[0].toLowerCase(); tag = tokens[1];
                // Si la palabra no pertenece al corpus la anadimos junto al tag asignado inicializando
                // el numero de apariciones a 1	
                if(!corpus.containsKey(word)) {
                    HashMap<String, Integer> tags = new HashMap<String, Integer>();
                    tags.put(tokens[1], 1);
                    corpus.put(tokens[0], tags);
                }
                // Si la palabra esta registrada en el corpus...
                else {
                    HashMap<String, Integer> tags = corpus.get(word);
                    // Si la palabra ya tenia el tag asignado, incrementamos el numero de apariciones
                    // para dicho tag
                    if (tags.containsKey(tag)) {
                        times = tags.get(tag) + 1;
                        tags.put(tag, times);
                    }
                    // En caso contrario, anadimos uno nuevo inicializandolo a 1
                    else {
                	tags.put(tag,1);
                    } 
            	}
            	// creamos el archivo que almacenara el corpus contabilizado
	        File fichero = new File("./Model.txt");
                if (fichero.exists()) fichero.delete();
                BufferedWriter text = new BufferedWriter(new OutputStreamWriter(new FileOutputStream("./Model.txt", true), "utf-8"));
                // Escribimos en el para cada palabra, sus tags y las apariciones de la palabra asociada a ese tag
                for (Iterator i = corpus.entrySet().iterator(); i.hasNext();) {
                    Map.Entry wordtags = (Map.Entry) i.next();
                    HashMap <String, Integer> tagstimes = (HashMap <String, Integer>) wordtags.getValue();
                    for (Iterator j = tagstimes.entrySet().iterator(); j.hasNext();){
                        Map.Entry tagtimes = (Map.Entry) j.next();
                        // wordtags.getKey() := palabra
                        // tagtimes.getKey() := tag de la palabra
                        // tagtimes.getValue() := apariciones del tag asociado a la palabra
			text.write((String)wordtags.getKey() + "\t" + (String)tagtimes.getKey() + "\t" + (Integer)tagtimes.getValue() + "\n");
                    }
                }
                // concluimos con la escritura
	       	text.close();
            }
        }            
	catch (UnsupportedEncodingException ex) {
	    Logger.getLogger(PLN1.class.getName()).log(Level.SEVERE, null, ex);
	} 
	catch (FileNotFoundException ex) {
	    Logger.getLogger(PLN1.class.getName()).log(Level.SEVERE, null, ex);
	} 
	catch (IOException ex) {
	    Logger.getLogger(PLN1.class.getName()).log(Level.SEVERE, null, ex);
	}
    }

    static void Tagging(String path) throws FileNotFoundException, UnsupportedEncodingException {
        HashMap< String, HashMap<String, Integer>> corpus = getCorpus("./Model.txt");
        File file = new File(path.replace(".txt","tagged.txt"));
        if (file.exists()) file.delete();
        try {
        	// Preparamos el nuevo fichero para taggearlo palabra por palabra a traves del anterior
            BufferedWriter taggedtext = new BufferedWriter(new OutputStreamWriter(new FileOutputStream(path.replace(".txt","tagged.txt"), true), "ISO-8859-1"));
            BufferedReader text = new BufferedReader(new InputStreamReader(new FileInputStream(path), "ISO-8859-1"));
            String line, wordLC, word, tag = "", previoustag = "";
            int times, maxtimes = 0;
            while ((line = text.readLine()) != null) {
                String[] words = line.split("\t");
                word = words[0]; wordLC = words[0].toLowerCase();
                // Si la palabra esta en el corpus...
                if (corpus.containsKey(wordLC)) {
                    HashMap<String, Integer> tagstimes = corpus.get(wordLC);
                    maxtimes = 0;
                    for(Iterator i = tagstimes.entrySet().iterator(); i.hasNext();){
                    	Map.Entry tagtimes = (Map.Entry) i.next();
                        times = (Integer) tagtimes.getValue();
                        if (maxtimes < times) {
                            maxtimes = times;
                            // Sacamos el tag con mas frecuencia asociado a la palabra
                            tag = (String) tagtimes.getKey();
                        }	
                    }
                    // actualizamos el tag para el analisis contextual
                    previoustag = tag;
                    taggedtext.write(word + "\t" + tag + "\n");
                } 
                else {
                	// En caso que no este en el corpus a traves de las siguientes reglas
                	// definimos el tag a la palabra
                	if (previoustag.equals("V")) taggedtext.write(word + "\t" + "Prep" + "\n");
                	else if(previoustag.equals("Det")) taggedtext.write(word + "\t" + "NC" + "\n");
                	else if (previoustag.equals("Pron")) taggedtext.write(word + "\t" + "V" + "\n"); 
                	else if(Character.isDigit(word.charAt(0))) taggedtext.write(word + "\t" + "Num" + "\n");	
                	else if(Character.isUpperCase(word.charAt(0))) taggedtext.write(word + "\t" + "NP" + "\n");
                	else {
                		// Corregimos la palabra por si hay diferencias con la original 
                		// en caso que hubiese alguna acentuacion
                        String correctword = correction(word, corpus);
                        if (correctword == null) taggedtext.write(word + "\t" + "Undefined" + "\r\n");
                        else {
                        	// Una vez corregida comprobamos el tag con mas frecuencia para esa palabra
                            HashMap<String, Integer> tagstimes = corpus.get(correctword);
                            maxtimes = 0;
                            for (Iterator i = tagstimes.entrySet().iterator(); i.hasNext();) {
                                Map.Entry tagtimes = (Map.Entry) i.next();
                                times = (Integer) tagtimes.getValue();
                                if (maxtimes < times) {
                                    maxtimes = times;
                                    tag = (String) tagtimes.getKey();
                                }
                            }
                            previoustag = tag;
                            // y volvemos a escribir en el fichero
                            taggedtext.write(word + "\t" + tag + "\r\n");
                        }
                    }
                }
            }
            text.close();
        } 
        catch (IOException e) {
        }
    }

    static String correction(String word, HashMap< String, HashMap< String, Integer>> corpus) {
        for (Map.Entry wordtags : corpus.entrySet()) {
            String corpusword = (String) wordtags.getKey();
            // Si la palabra y la del corpus a comparar tiene no coinciden en 2 o mas caracteres no es la misma
            // de ser un caracter diferente estariamos dando con una posible tilde
            if (word.length() == corpusword.length()) if (word.compareToIgnoreCase(corpusword) > -2) return corpusword;                
        }
        return null;
    }

    static HashMap <String, HashMap <String, Integer>> getCorpus(String path) throws FileNotFoundException {
        HashMap <String, HashMap <String, Integer>> corpus = new HashMap <String, HashMap <String,Integer>>();
        String line, word, tag;
        int times;
        BufferedReader file = new BufferedReader(new FileReader(path));
        try {
 			// Revisamos linea a linea hasta que el archivo este vacio
            while ((line = file.readLine()) != null) {
            	// Para cada linea revisamos separamos e identificamos cada termino
                String[] tokens = line.split("\t");
                word = tokens[0]; tag = tokens[1]; times = new Integer(tokens[2]);
                // Introducimos nueva palabra con tag asignado y numero de apariciones
                if(!corpus.containsKey(word)) {
                    HashMap<String, Integer> tags = new HashMap<String, Integer>();
                    tags.put(tag, times);
                    corpus.put(word, tags);
                }
                // Introducimos nuevo tag y apariciones dada una palabra existente
                else {
                    HashMap<String, Integer> tags = corpus.get(word);
                    tags.put(tag, times);
                }
            }
            return corpus;
        } 
        catch (IOException e) {
        }
        return null;
    }

    static double Avaluation(String path1, String path2) {
        double hits = 0, undefineds = 0, misses = 0, total = 0, score = 0;
        try {
            // text 1 contiene el texto etiquetado, el text 2 contiene el que tiene la etiquetacion optima
            BufferedReader text1 = new BufferedReader(new InputStreamReader(new FileInputStream(path1), "ISO-8859-1"));
            BufferedReader text2 = new BufferedReader(new InputStreamReader(new FileInputStream(path2), "ISO-8859-1"));
            String line1, line2;

            while ((line1 = text1.readLine()) != null && (line2 = text2.readLine()) != null) {
                String[] words1 = line1.split("\t");
                String[] words2 = line2.split("\t");
                // Si los tags coinciden en la misma palabra incrementamos el numero de aciertos
                if (words1[0].equalsIgnoreCase(words2[0]) && words1[1].equals(words2[1])) ++hits;
                // En caso que los tags no coincidan, es fallo de tag
                else if(words1[0].equalsIgnoreCase(words2[0]) && words1[1].equals(words2[1])) ++misses;
                // En caso de que el tag no este definido porque no existe en el corpus error tambien
                else if (words1[1].equals("Undefined")) ++undefineds;
                // Comprobamos que todas las palabras no estan correctamente etiquetadas
                else if (!words1[0].equalsIgnoreCase(words2[0]) && words1[1].equals(words2[1])) {
                   System.out.println("Error! " + words1[0] + " y " + words2[0] + " etiquetadas como " + words1[1] + "\n");
                }
                ++total;
            }
            score = (hits / total);
	        System.out.println(path1 + " evaluado, " + score*100 + "% de acierto en el etiquetado de " + total + "palabras.");
	        System.out.println("Resumen:");
	        System.out.println("Palabras correctamente etiquetadas: " + hits + "/" + total);
	        System.out.println("Palabras incorrectamente etiquetadas: " + misses + "/" + total);
	        System.out.println("Palabras no identificadas: " + undefineds + "/" + total);
	        return score;
        } 
        catch (IOException e) {
        }
        return 0;
    }
}