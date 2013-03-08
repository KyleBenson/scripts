/** An example of synchronization in Java. I put comments in several places to illustrated the different possible ways of
accomplishing synchronization.  Leave everything commented out to see how the value of the counter may not be as expected.

@author: Kyle Benson
Winter 2013
CS 143A - Principles of Operating Systems
*/

import java.util.Vector;
import java.util.concurrent.Semaphore;

public class SynchronizationExample {
    static final int numThreads = 100;
    private static final Semaphore semaphore = new Semaphore(1); //1 means mutex

    public static class Counter {
	private int count;
	public Counter(int start){
	    this.count = start;
	}

	//We can synchronize this function in several ways.
	public /*synchronized*/ void increment(){
	    //synchronized(this) {
	    this.count++; //this operation is not atomic and can lead to corruption of this.count!
	    //}
	}

	//If we were accessing this from threads instead of main,
	//we would want to synchronize it as well.
	public int getCount(){
	    return count;
	}
    }

    /** This threaded class will simply increment a shared variable. */
    public static class CountingThread implements Runnable {
	private Counter sharedVar;

	public CountingThread (Counter theSharedVar) {
	    sharedVar = theSharedVar;
	}

	public void run() {
	    try {
		Thread.sleep(1000);
	    }
	    catch (InterruptedException e) {
		System.out.println("Interrupted!");
	    }

	    //We need to make sure we release the semaphore (in the finally block) if one of the threads dies!
	    /*try {
	      semaphore.acquire();*/
		sharedVar.increment();
		/*}
	    catch (InterruptedException e) {}
	    finally {
		semaphore.release();
		}*/

		//Alternatively, we can use a synchronized block here instead of handling synchronization in the counter or with a semaphore.

		/*synchronized(this.sharedVar) {
		    sharedVar.increment();
		}*/
	}
    }

    public static void main(String args[]){
	Counter sharedVar = new Counter(0); //should be == numThreads when finished is synched properly.
	Vector<Thread> myThreads = new Vector<Thread>();

	//Create thread objects wrapping our class defined above
	for (int i = 0; i < numThreads; i++) {
	    myThreads.add(new Thread(new CountingThread(sharedVar)));
	}

	for (Thread t : myThreads) {
	    t.start();
	}
	
	for (Thread t : myThreads) {
	    try {
		t.join();
	    }
	    catch (InterruptedException e) {
		System.out.println("Interrupted!");
	    }
	}

	System.out.format("Expecting sharedVar = %d\n", numThreads);
	System.out.format("Actual sharedVar = %d\n", sharedVar.getCount());
    }
}